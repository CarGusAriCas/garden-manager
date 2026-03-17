"""
Utilidades para detección de dispositivo y layout responsive.
Inyecta JavaScript para detectar el ancho de pantalla del cliente.
"""
import streamlit as st
import streamlit.components.v1 as components


def detect_device() -> str:
    """
    Detecta el tipo de dispositivo mediante JavaScript.
    Devuelve 'mobile', 'tablet' o 'desktop'.
    """
    # Inyecta JS que escribe el ancho en un elemento oculto
    components.html("""
        <script>
            const width = window.innerWidth;
            let device = 'desktop';
            if (width < 768) device = 'mobile';
            else if (width < 1024) device = 'tablet';

            // Guarda en sessionStorage para persistir
            sessionStorage.setItem('device_type', device);
            sessionStorage.setItem('screen_width', width);

            // Envía al padre (Streamlit) via postMessage
            window.parent.postMessage({
                type: 'device_info',
                device: device,
                width: width
            }, '*');
        </script>
    """, height=0)

    # Recupera de query params si está disponible
    params = st.query_params
    return params.get("device", "desktop")


def get_columns(mobile: int = 1, tablet: int = 2, desktop: int = 3) -> int:
    """
    Devuelve el número de columnas apropiado según el dispositivo.

    Args:
        mobile: Columnas en móvil (por defecto 1)
        tablet: Columnas en tablet (por defecto 2)
        desktop: Columnas en escritorio (por defecto 3)

    Returns:
        Número de columnas para el dispositivo actual
    """
    device = st.session_state.get("device", "desktop")
    if device == "mobile":
        return mobile
    elif device == "tablet":
        return tablet
    return desktop


def apply_responsive_css():
    """
    Aplica CSS responsive global para mejorar la visualización
    en dispositivos móviles y tablets.
    """
    st.markdown("""
        <style>
        /* ── Móvil ──────────────────────────────────────── */
        @media (max-width: 768px) {
            /* Oculta sidebar en móvil por defecto */
            [data-testid="stSidebar"] {
                width: 0 !important;
                min-width: 0 !important;
            }

            /* Reduce padding en móvil */
            .block-container {
                padding: 1rem !important;
                max-width: 100% !important;
            }

            /* Botones más grandes para táctil */
            .stButton button {
                min-height: 48px !important;
                font-size: 16px !important;
            }

            /* Inputs más grandes */
            .stTextInput input,
            .stSelectbox select {
                min-height: 44px !important;
                font-size: 16px !important;
            }

            /* Métricas apiladas */
            [data-testid="metric-container"] {
                width: 100% !important;
            }

            /* Oculta elementos secundarios en móvil */
            .hide-mobile {
                display: none !important;
            }
        }

        /* ── Tablet ─────────────────────────────────────── */
        @media (min-width: 769px) and (max-width: 1024px) {
            .block-container {
                padding: 1.5rem !important;
                max-width: 100% !important;
            }

            .stButton button {
                min-height: 44px !important;
            }
        }

        /* ── Desktop ────────────────────────────────────── */
        @media (min-width: 1025px) {
            .block-container {
                max-width: 1400px !important;
            }
        }

        /* ── Global ─────────────────────────────────────── */
        /* Mejora legibilidad en todas las pantallas */
        .stMarkdown p {
            line-height: 1.6 !important;
        }

        /* Contenedores con borde más compactos en móvil */
        [data-testid="stVerticalBlockBorderWrapper"] {
            padding: 0.5rem !important;
        }

        /* Mejora tablas en móvil */
        .stDataFrame {
            overflow-x: auto !important;
        }
        </style>
    """, unsafe_allow_html=True)


def device_selector():
    """
    Widget de selección manual de dispositivo para pruebas.
    Solo visible en modo debug.
    """
    if st.session_state.get("debug_mode"):
        device = st.sidebar.selectbox(
            "🔧 Simular dispositivo",
            ["desktop", "tablet", "mobile"],
            index=["desktop", "tablet", "mobile"].index(
                st.session_state.get("device", "desktop")
            )
        )
        st.session_state["device"] = device