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


def mobile_topbar():
    """
    Muestra una barra de navegación superior en móvil.
    Solo visible cuando device == 'mobile'.
    Oculta la sidebar completamente.
    """
    device = st.session_state.get("device", "desktop")
    if device != "mobile":
        return

    # Oculta sidebar en móvil
    st.markdown("""
        <style>
        [data-testid="stSidebar"] { display: none !important; }
        [data-testid="collapsedControl"] { display: none !important; }
        .block-container { padding-top: 0.5rem !important; }
        </style>
    """, unsafe_allow_html=True)

    # ── Fila 1 — Atrás + Logo + Sugerencias ───────────────────
    col_back, col_title, col_suggest = st.columns([1, 5, 1])
    with col_back:
        if st.button("◀", key="topbar_back", use_container_width=True):
            st.switch_page("Home.py")
    with col_title:
        st.markdown("**🌿 GardenManager**")
    with col_suggest:
        if st.button("💡", key="topbar_suggest", use_container_width=True):
            st.switch_page("pages/08_Sugerencias.py")

    # ── Fila 2 — Navegación principal ─────────────────────────
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        if st.button("👤\nClientes",  key="top_cli", use_container_width=True):
            st.switch_page("pages/01_Clientes.py")
    with c2:
        if st.button("👷\nEmpleados", key="top_emp", use_container_width=True):
            st.switch_page("pages/02_Empleados.py")
    with c3:
        if st.button("📅\nTareas",    key="top_tar", use_container_width=True):
            st.switch_page("pages/03_Tareas.py")
    with c4:
        if st.button("🏖️\nAusencias", key="top_aus", use_container_width=True):
            st.switch_page("pages/04_Ausencias.py")

    # ── Fila 3 — Navegación secundaria ────────────────────────
    c5, c6, c7, c8 = st.columns(4)
    with c5:
        if st.button("📋\nTrabajos",  key="top_job", use_container_width=True):
            st.switch_page("pages/05_Trabajos.py")
    with c6:
        if st.button("🗺️\nMapa",      key="top_map", use_container_width=True):
            st.switch_page("pages/06_Mapa.py")
    with c7:
        if st.button("🧭\nRutas",     key="top_rut", use_container_width=True):
            st.switch_page("pages/07_Mapa_Empleados.py")
    with c8:
        if st.button("🏠\nInicio",    key="top_hom", use_container_width=True):
            st.switch_page("Home.py")

    st.divider()


def back_button(label: str = "◀ Volver al inicio"):
    """
    Muestra un botón de volver en desktop y tablet.
    En móvil no hace falta porque ya está en la topbar.
    """
    device = st.session_state.get("device", "desktop")
    if device == "mobile":
        return
    if st.button(label, key="back_btn"):
        st.switch_page("Home.py")