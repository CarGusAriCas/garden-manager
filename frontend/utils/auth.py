"""
Utilidades de autenticación para Streamlit.
Gestiona el estado de sesión del usuario.
"""
import streamlit as st


def init_auth():
    """Inicializa las variables de autenticación en session_state."""
    if "authenticated" not in st.session_state:
        st.session_state["authenticated"]        = False
        st.session_state["token"]                = None
        st.session_state["role"]                 = None
        st.session_state["nombre"]               = None
        st.session_state["must_change_password"] = False


def is_authenticated() -> bool:
    """Verifica si el usuario está autenticado."""
    return st.session_state.get("authenticated", False)


def get_role() -> str:
    """Devuelve el rol del usuario actual."""
    return st.session_state.get("role", "")


def get_nombre() -> str:
    """Devuelve el nombre del usuario actual."""
    return st.session_state.get("nombre", "")


def logout():
    """Cierra la sesión del usuario."""
    for key in ["authenticated", "token", "role", "nombre", "must_change_password"]:
        st.session_state[key] = None
    st.session_state["authenticated"] = False


def require_auth(roles: list = None, pagina: str = ""):
    """
    Verifica autenticación y rol.
    Si no está autenticado redirige al Home.
    Si no tiene el rol requerido muestra error con opción de solicitar acceso.
    """
    init_auth()

    if not is_authenticated():
        st.switch_page("Home.py")
        st.stop()

    if roles and get_role() not in roles:
        st.error("🚫 No tienes permisos para acceder a esta sección.")
        st.info(f"Tu rol actual es: **{get_role()}**. Esta sección requiere: **{', '.join(roles)}**")

        if st.button("📧 Solicitar acceso al administrador", use_container_width=True):
            from utils.api_client import solicitar_acceso
            solicitar_acceso(
                pagina     = pagina or "sección desconocida",
                usuario    = get_nombre(),
                rol_actual = get_role()
            )
            st.success("✅ Solicitud enviada al administrador.")

        st.stop()


def get_employee_id() -> int | None:
    """Devuelve el employee_id del usuario actual si está vinculado."""
    return st.session_state.get("employee_id")


def is_admin_or_encargado() -> bool:
    """Verifica si el usuario tiene rol de admin o encargado."""
    return get_role() in ["admin", "encargado"]