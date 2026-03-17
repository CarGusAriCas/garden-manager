"""
Página de gestión de empleados.
"""
import streamlit as st
import sys
import os
from datetime import date
from utils.responsive import apply_responsive_css, mobile_topbar, back_button
from utils.api_client import get_employees, create_employee, update_employee, delete_employee, format_date_es

apply_responsive_css()
mobile_topbar()
back_button()


sys.path.append(os.path.dirname(os.path.dirname(__file__)))


st.set_page_config(page_title="Empleados · GardenManager", page_icon="👷", layout="wide")
st.title("👷 Gestión de Empleados")
st.divider()

ROLES        = ["Jardinero", "Jardinera", "Encargado", "Encargada", "Auxiliar"]
ESPECIALIDADES = ["Poda y mantenimiento", "Sistemas de riego", "Diseño floral",
                  "Jardinería general", "Tratamientos fitosanitarios", "Césped y siembra"]

tab_lista, tab_nuevo = st.tabs(["📋 Lista de empleados", "➕ Nuevo empleado"])

# ── Tab: Lista ─────────────────────────────────────────────────
with tab_lista:
    try:
        empleados = get_employees()
        if not empleados:
            st.info("No hay empleados registrados.")
        else:
            st.caption(f"{len(empleados)} empleados activos")

            for e in empleados:
                with st.expander(f"👷 {e['name']}  —  {e.get('role', '')}"):
                    col1, col2 = st.columns(2)

                    with col1:
                        st.markdown(f"**📧 Email:** {e.get('email') or '—'}")
                        st.markdown(f"**📞 Teléfono:** {e.get('phone') or '—'}")
                        st.markdown(f"**🌿 Especialidad:** {e.get('speciality') or '—'}")
                        hire = e.get('hire_date')
                        st.markdown(f"**📅 Incorporación:** {format_date_es(hire) if hire else '—'}")

                    with col2:
                        st.markdown("**✏️ Editar empleado**")
                        with st.form(key=f"edit_emp_{e['id']}"):
                            new_name  = st.text_input("Nombre",       value=e['name'])
                            new_phone = st.text_input("Teléfono",     value=e.get('phone') or "")
                            new_email = st.text_input("Email",        value=e.get('email') or "")
                            new_role  = st.selectbox("Rol", ROLES,
                                index=ROLES.index(e['role']) if e['role'] in ROLES else 0)
                            new_spec  = st.text_input("Especialidad", value=e.get('speciality') or "")

                            col_save, col_del = st.columns(2)
                            with col_save:
                                if st.form_submit_button("💾 Guardar", use_container_width=True):
                                    try:
                                        update_employee(e['id'], {
                                            "name":      new_name,
                                            "phone":     new_phone or None,
                                            "email":     new_email or None,
                                            "role":      new_role,
                                            "speciality":new_spec  or None,
                                        })
                                        st.success("Empleado actualizado.")
                                        st.rerun()
                                    except Exception as ex:
                                        st.error(f"Error: {ex}")
                            with col_del:
                                if st.form_submit_button("🗑️ Desactivar", use_container_width=True):
                                    try:
                                        delete_employee(e['id'])
                                        st.warning("Empleado desactivado.")
                                        st.rerun()
                                    except Exception as ex:
                                        st.error(f"Error: {ex}")

    except Exception as e:
        st.error(f"❌ Error al cargar empleados: {e}")

# ── Tab: Nuevo empleado ────────────────────────────────────────
with tab_nuevo:
    st.subheader("Registrar nuevo empleado")
    with st.form("form_nuevo_empleado"):
        name      = st.text_input("Nombre completo *", placeholder="Carlos Ruiz")
        phone     = st.text_input("Teléfono",          placeholder="634 567 890")
        email     = st.text_input("Email",             placeholder="carlos@jardineria.com")
        role      = st.selectbox("Rol *", ROLES)
        speciality= st.selectbox("Especialidad", ESPECIALIDADES)
        hire_date = st.date_input("Fecha de incorporación", value=date.today())

        submitted = st.form_submit_button("➕ Crear empleado", use_container_width=True)

        if submitted:
            if not name:
                st.error("El nombre es obligatorio.")
            else:
                try:
                    create_employee({
                        "name":       name,
                        "phone":      phone      or None,
                        "email":      email      or None,
                        "role":       role,
                        "speciality": speciality or None,
                        "hire_date":  str(hire_date),
                    })
                    st.success(f"✅ Empleado '{name}' creado correctamente.")
                    st.rerun()
                except Exception as ex:
                    st.error(f"❌ Error: {ex}")