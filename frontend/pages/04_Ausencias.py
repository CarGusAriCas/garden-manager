"""
Página de gestión de ausencias de personal.
"""
import streamlit as st
import sys
import os
from datetime import date
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from utils.api_client import (
    get_absences, get_employees, create_absence,
    update_absence, check_availability, format_date_es
)

st.set_page_config(page_title="Ausencias · GardenManager", page_icon="🏖️", layout="wide")
st.title("🏖️ Control de Ausencias")
st.divider()

TIPOS_AUSENCIA = ["vacaciones", "baja_medica", "asunto_personal", "otro"]

tab_lista, tab_nueva, tab_disponibilidad = st.tabs([
    "📋 Ausencias registradas",
    "➕ Registrar ausencia",
    "✅ Comprobar disponibilidad"
])

# ── Tab: Lista ─────────────────────────────────────────────────
with tab_lista:
    try:
        ausencias = get_absences()
        if not ausencias:
            st.info("No hay ausencias registradas.")
        else:
            st.caption(f"{len(ausencias)} ausencias registradas")
            for a in ausencias:
                nombre   = a.get("employee", {}).get("name", "—")
                aprobada = "✅ Aprobada" if a["is_approved"] else "⏳ Pendiente de aprobación"
                with st.expander(f"👷 {nombre}  —  {a['absence_type']}  —  {aprobada}"):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.markdown(f"**📅 Inicio:** {format_date_es(str(a['start_date']))}")
                        st.markdown(f"**📅 Fin:** {format_date_es(str(a['end_date']))}")
                        st.markdown(f"**📝 Motivo:** {a.get('reason') or '—'}")
                    with col2:
                        st.markdown("**✏️ Gestionar**")
                        with st.form(key=f"abs_{a['id']}"):
                            aprobado = st.checkbox("Marcar como aprobada",
                                value=a["is_approved"])
                            nuevo_motivo = st.text_area("Motivo",
                                value=a.get("reason") or "")
                            if st.form_submit_button("💾 Guardar", use_container_width=True):
                                try:
                                    update_absence(a['id'], {
                                        "is_approved": aprobado,
                                        "reason":      nuevo_motivo or None,
                                    })
                                    st.success("Ausencia actualizada.")
                                    st.rerun()
                                except Exception as ex:
                                    st.error(f"Error: {ex}")
    except Exception as e:
        st.error(f"❌ Error al cargar ausencias: {e}")

# ── Tab: Nueva ausencia ────────────────────────────────────────
with tab_nueva:
    st.subheader("Registrar nueva ausencia")
    try:
        empleados = get_employees()
        empleados_opciones = {e['name']: e['id'] for e in empleados}

        with st.form("form_nueva_ausencia"):
            empleado   = st.selectbox("Empleado *", list(empleados_opciones.keys()))
            tipo       = st.selectbox("Tipo de ausencia *", TIPOS_AUSENCIA)
            col1, col2 = st.columns(2)
            with col1:
                inicio = st.date_input("Fecha de inicio *", value=date.today())
            with col2:
                fin    = st.date_input("Fecha de fin *",    value=date.today())
            motivo = st.text_area("Motivo", placeholder="Descripción opcional...")

            submitted = st.form_submit_button("➕ Registrar ausencia", use_container_width=True)

            if submitted:
                if fin < inicio:
                    st.error("La fecha de fin no puede ser anterior a la de inicio.")
                else:
                    try:
                        create_absence({
                            "employee_id":  empleados_opciones[empleado],
                            "absence_type": tipo,
                            "start_date":   str(inicio),
                            "end_date":     str(fin),
                            "reason":       motivo or None,
                        })
                        st.success(f"✅ Ausencia de '{empleado}' registrada correctamente.")
                        st.rerun()
                    except Exception as ex:
                        st.error(f"❌ Error: {ex}")

    except Exception as e:
        st.error(f"❌ Error: {e}")

# ── Tab: Disponibilidad ────────────────────────────────────────
with tab_disponibilidad:
    st.subheader("Comprobar disponibilidad de empleado")
    try:
        empleados = get_employees()
        empleados_opciones = {e['name']: e['id'] for e in empleados}

        col1, col2 = st.columns(2)
        with col1:
            empleado_sel = st.selectbox("Empleado", list(empleados_opciones.keys()))
        with col2:
            fecha_check  = st.date_input("Fecha a comprobar", value=date.today())

        if st.button("✅ Comprobar disponibilidad", use_container_width=True):
            try:
                resultado = check_availability(
                    empleados_opciones[empleado_sel], fecha_check
                )
                if resultado["available"]:
                    st.success(f"✅ **{empleado_sel}** está **disponible** el {format_date_es(str(fecha_check))}")
                else:
                    st.error(f"❌ **{empleado_sel}** está **ausente** el {format_date_es(str(fecha_check))}")
            except Exception as ex:
                st.error(f"Error: {ex}")

    except Exception as e:
        st.error(f"❌ Error: {e}")