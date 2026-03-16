"""
Página principal de GardenManager.
Muestra un resumen del estado actual del negocio.
"""
import streamlit as st
import sys
import os

# Añade el directorio frontend al path para importar utils
sys.path.append(os.path.dirname(__file__))
from utils.api_client import get_clients, get_employees, get_tasks, get_jobs, get_absences

st.set_page_config(
    page_title="GardenManager",
    page_icon="🌿",
    layout="wide"
)

st.title("🌿 GardenManager")
st.caption("Panel de control · Empresa de jardinería")
st.divider()

# ── Métricas principales ───────────────────────────────────────
try:
    clientes  = get_clients()
    empleados = get_employees()
    tareas    = get_tasks()
    trabajos  = get_jobs()
    ausencias = get_absences()

    col1, col2, col3, col4, col5 = st.columns(5)

    col1.metric("👤 Clientes",   len(clientes))
    col2.metric("👷 Empleados",  len(empleados))
    col3.metric("📅 Tareas",     len(tareas))
    col4.metric("📋 Trabajos",   len(trabajos))
    col5.metric("🏖️ Ausencias",  len(ausencias))

    st.divider()

    # ── Tareas pendientes ──────────────────────────────────────
    col_left, col_right = st.columns(2)

    with col_left:
        st.subheader("📅 Tareas pendientes")
        pendientes = [t for t in tareas if t["status"] == "pendiente"]
        if pendientes:
            for t in pendientes[:5]:
                with st.container(border=True):
                    st.markdown(f"**{t['title']}**")
                    st.caption(f"📆 {t['date']} · 🔺 Prioridad: {t['priority']}")
        else:
            st.info("No hay tareas pendientes.")

    with col_right:
        st.subheader("🏖️ Ausencias activas")
        if ausencias:
            for a in ausencias[:5]:
                with st.container(border=True):
                    nombre = a.get("employee", {}).get("name", "Empleado")
                    st.markdown(f"**{nombre}**")
                    st.caption(f"📆 {a['start_date']} → {a['end_date']} · {a['absence_type']}")
        else:
            st.info("No hay ausencias registradas.")

except Exception as e:
    st.error(f"❌ No se puede conectar con el servidor. ¿Está el backend activo?\n\n{e}")