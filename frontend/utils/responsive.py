"""
Utilidades responsive para GardenManager.
Detecta dispositivo y adapta la interfaz.
"""
import streamlit as st
import streamlit.components.v1 as components


def apply_responsive_css():
    """Aplica CSS responsive global."""
    st.markdown("""
        <style>
        @media (max-width: 768px) {
            .block-container {
                padding: 1rem !important;
                max-width: 100% !important;
            }
            .stButton button {
                min-height: 48px !important;
                font-size: 16px !important;
            }
            .stTextInput input {
                min-height: 44px !important;
                font-size: 16px !important;
            }
            .hide-mobile { display: none !important; }
        }
        @media (min-width: 769px) and (max-width: 1024px) {
            .block-container {
                padding: 1.5rem !important;
                max-width: 100% !important;
            }
        }
        @media (min-width: 1025px) {
            .block-container { max-width: 1400px !important; }
        }
        .stMarkdown p { line-height: 1.6 !important; }
        .stDataFrame { overflow-x: auto !important; }
        </style>
    """, unsafe_allow_html=True)


def init_device():
    """
    Inicializa la detección de dispositivo.
    Usa un componente HTML que lee el ancho y lo guarda en query params.
    Solo se ejecuta en Home.py una vez por sesión.
    """
    if "device_detected" in st.session_state:
        return

    # Lee query param si ya está seteado
    params = st.query_params
    if "device" in params:
        device = params["device"]
        st.session_state["device"] = device
        st.session_state["device_detected"] = True
        return

    # Inyecta JS que detecta y redirige UNA sola vez
    components.html("""
        <script>
            const w = window.parent.innerWidth;
            let d = 'desktop';
            if (w < 768) d = 'mobile';
            else if (w < 1024) d = 'tablet';

            const url = new URL(window.parent.location.href);
            url.searchParams.set('device', d);
            window.parent.location.replace(url.toString());
        </script>
    """, height=0)


def mobile_topbar():
    """
    Topbar de navegación para móvil.
    Lee el device desde query params directamente.
    """
    # Lee device desde query params o session_state
    params = st.query_params
    if "device" in params:
        st.session_state["device"] = params["device"]

    device = st.session_state.get("device", "desktop")
    if device != "mobile":
        return

    # Oculta sidebar completamente
    st.markdown("""
        <style>
        [data-testid="stSidebar"],
        [data-testid="collapsedControl"] {
            display: none !important;
        }
        .block-container {
            padding-top: 0.5rem !important;
        }
        </style>
    """, unsafe_allow_html=True)

    # Fila 1 — Atrás + título + sugerencias
    c_back, c_title, c_sug = st.columns([1, 5, 1])
    with c_back:
        if st.button("◀", key="tb_back", use_container_width=True):
            st.switch_page("Home.py")
    with c_title:
        st.markdown("**🌿 GardenManager**")
    with c_sug:
        if st.button("💡\nSugerencias", key="tb_sug", use_container_width=True):
            st.switch_page("pages/08_Sugerencias.py")

    # Fila 2 — navegación principal
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        if st.button("👤\nClientes",  key="tb_cli", use_container_width=True):
            st.switch_page("pages/01_Clientes.py")
    with c2:
        if st.button("👷\nEmpleados", key="tb_emp", use_container_width=True):
            st.switch_page("pages/02_Empleados.py")
    with c3:
        if st.button("📅\nTareas",    key="tb_tar", use_container_width=True):
            st.switch_page("pages/03_Tareas.py")
    with c4:
        if st.button("🏖️\nAusencias", key="tb_aus", use_container_width=True):
            st.switch_page("pages/04_Ausencias.py")

    # Fila 3 — navegación secundaria
    c5, c6, c7, c8 = st.columns(4)
    with c5:
        if st.button("📋\nTrabajos",  key="tb_job", use_container_width=True):
            st.switch_page("pages/05_Trabajos.py")
    with c6:
        if st.button("🗺️\nMapa",      key="tb_map", use_container_width=True):
            st.switch_page("pages/06_Mapa.py")
    with c7:
        if st.button("🧭\nRutas",     key="tb_rut", use_container_width=True):
            st.switch_page("pages/07_Mapa_Empleados.py")
    with c8:
        if st.button("🏠\nInicio",    key="tb_hom", use_container_width=True):
            st.switch_page("Home.py")

    st.divider()


def back_button(label: str = "◀ Volver al inicio"):
    """Botón de volver para desktop y tablet."""
    device = st.session_state.get("device", "desktop")
    if device == "mobile":
        return
    if st.button(label, key="back_btn"):
        st.switch_page("Home.py")


def device_selector():
    """Selector manual de dispositivo en el sidebar."""
    st.sidebar.markdown("### 🌿 GardenManager")
    st.sidebar.divider()

    device_actual = st.session_state.get("device", "desktop")
    opciones      = ["auto", "desktop", "tablet", "mobile"]
    idx           = opciones.index(device_actual) if device_actual in opciones else 0

    seleccion = st.sidebar.selectbox(
        "🔧 Vista",
        opciones,
        index=idx,
        label_visibility="collapsed"
    )

    if seleccion != "auto":
        st.session_state["device"] = seleccion
    elif "device" not in st.session_state:
        st.session_state["device"] = "desktop"

    st.sidebar.divider()
    if st.sidebar.button("💡 Sugerencias", use_container_width=True):
        st.switch_page("pages/08_Sugerencias.py")