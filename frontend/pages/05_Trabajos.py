"""
Página de gestión de trabajos y checklists.
"""
import streamlit as st
import sys
import os
from utils.responsive import apply_responsive_css, mobile_topbar, back_button
from datetime import datetime
from utils.api_client import (
    get_jobs, get_tasks, create_job,
    update_job, update_checklist_item, format_date_es
)

apply_responsive_css()
mobile_topbar()
back_button()

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

st.set_page_config(page_title="Trabajos · GardenManager", page_icon="📋", layout="wide")
st.title("📋 Trabajos realizados")
st.divider()

ESTADOS_JOB = ["en_progreso", "completado", "incompleto"]

tab_lista, tab_nuevo = st.tabs(["📋 Lista de trabajos", "➕ Registrar trabajo"])

# ── Tab: Lista ─────────────────────────────────────────────────
with tab_lista:
    try:
        trabajos = get_jobs()
        if not trabajos:
            st.info("No hay trabajos registrados todavía.")
        else:
            st.caption(f"{len(trabajos)} trabajos registrados")

            for j in trabajos:
                estado_icon = "🟢" if j["status"] == "completado" else \
                              "🟡" if j["status"] == "en_progreso" else "🔴"
                fecha = format_date_es(j["created_at"][:10])

                with st.expander(f"{estado_icon} Trabajo #{j['id']}  —  Tarea ID: {j['task_id']}  —  {fecha}"):
                    col1, col2 = st.columns(2)

                    with col1:
                        st.markdown(f"**📌 Estado:** {j['status']}")
                        inicio = j.get('started_at', '')
                        fin    = j.get('finished_at', '')
                        st.markdown(f"**🕐 Inicio:** {inicio[:16] if inicio else '—'}")
                        st.markdown(f"**🕑 Fin:** {fin[:16] if fin else '—'}")
                        st.markdown(f"**📝 Notas:** {j.get('notes') or '—'}")

                        # Checklist
                        st.divider()
                        st.markdown("**✅ Checklist**")
                        items = j.get("checklist_items", [])
                        if items:
                            for item in items:
                                done_icon = "✅" if item["is_done"] else "⬜"
                                inc_icon  = " 🚨" if item["has_incident"] else ""
                                st.markdown(f"{done_icon} {item['description']}{inc_icon}")
                                if item.get("incident_notes"):
                                    st.caption(f"   ⚠️ {item['incident_notes']}")
                        else:
                            st.caption("Sin ítems de checklist.")

                    with col2:
                        st.markdown("**✏️ Actualizar trabajo**")
                        with st.form(key=f"job_{j['id']}"):
                            nuevo_estado = st.selectbox("Estado", ESTADOS_JOB,
                                index=ESTADOS_JOB.index(j['status']) if j['status'] in ESTADOS_JOB else 0)
                            nuevas_notas = st.text_area("Notas", value=j.get('notes') or "")
                            fin_real     = st.checkbox("Marcar como finalizado ahora")

                            if st.form_submit_button("💾 Guardar", use_container_width=True):
                                try:
                                    data = {
                                        "status": nuevo_estado,
                                        "notes":  nuevas_notas or None,
                                    }
                                    if fin_real:
                                        data["finished_at"] = datetime.now().isoformat()
                                        data["status"]      = "completado"
                                    update_job(j['id'], data)
                                    st.success("Trabajo actualizado.")
                                    st.rerun()
                                except Exception as ex:
                                    st.error(f"Error: {ex}")

                        # Actualizar ítems del checklist
                        if items:
                            st.markdown("**✏️ Actualizar checklist**")
                            for item in items:
                                with st.form(key=f"item_{item['id']}"):
                                    st.caption(item['description'])
                                    col_a, col_b = st.columns(2)
                                    with col_a:
                                        is_done = st.checkbox("Completado",
                                            value=item['is_done'])
                                    with col_b:
                                        has_inc = st.checkbox("Incidencia",
                                            value=item['has_incident'])
                                    inc_notes = st.text_input("Descripción incidencia",
                                        value=item.get('incident_notes') or "")

                                    if st.form_submit_button("💾 Guardar ítem"):
                                        try:
                                            update_checklist_item(item['id'], {
                                                "is_done":       is_done,
                                                "has_incident":  has_inc,
                                                "incident_notes": inc_notes or None,
                                            })
                                            st.success("Ítem actualizado.")
                                            st.rerun()
                                        except Exception as ex:
                                            st.error(f"Error: {ex}")

    except Exception as e:
        st.error(f"❌ Error al cargar trabajos: {e}")

# ── Tab: Nuevo trabajo ─────────────────────────────────────────
with tab_nuevo:
    st.subheader("Registrar nuevo trabajo")
    try:
        tareas = get_tasks()
        if not tareas:
            st.warning("No hay tareas disponibles. Crea una tarea primero.")
        else:
            tareas_opciones = {
                f"#{t['id']} — {t['title']} ({format_date_es(t['date'])})": t['id']
                for t in tareas
            }

            with st.form("form_nuevo_trabajo"):
                tarea_sel   = st.selectbox("Tarea origen *", list(tareas_opciones.keys()))
                inicio_real = st.checkbox("Registrar hora de inicio ahora", value=True)
                notas       = st.text_area("Notas iniciales",
                    placeholder="Observaciones al comenzar el trabajo...")

                st.markdown("**Checklist inicial** — añade los ítems a verificar:")
                num_items = st.number_input("Número de ítems", min_value=0, max_value=10, value=3)

                items_desc = []
                for i in range(int(num_items)):
                    desc = st.text_input(f"Ítem {i+1}", key=f"item_desc_{i}",
                        placeholder=f"Descripción del ítem {i+1}")
                    items_desc.append(desc)

                submitted = st.form_submit_button("➕ Registrar trabajo", use_container_width=True)

                if submitted:
                    try:
                        checklist = [
                            {"description": d, "is_done": False, "has_incident": False}
                            for d in items_desc if d.strip()
                        ]
                        data = {
                            "task_id":        tareas_opciones[tarea_sel],
                            "status":         "en_progreso",
                            "notes":          notas or None,
                            "checklist_items": checklist,
                        }
                        if inicio_real:
                            data["started_at"] = datetime.now().isoformat()

                        create_job(data)
                        st.success("✅ Trabajo registrado correctamente.")
                        st.rerun()
                    except Exception as ex:
                        st.error(f"❌ Error: {ex}")

    except Exception as e:
        st.error(f"❌ Error al cargar tareas: {e}")