"""
Página de gestión de tareas y agenda semanal.
"""
import sys
import os
import streamlit as st
from datetime import date, timedelta

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from utils.auth import require_auth, get_employee_id, is_admin_or_encargado

st.set_page_config(page_title="Tareas · GardenManager", page_icon="📅", layout="wide")

require_auth()

# ── Filtro por rol ─────────────────────────────────────────────
es_admin = is_admin_or_encargado()
mi_employee_id = get_employee_id()

from utils.responsive import apply_responsive_css, mobile_topbar, back_button # noqa: E402
from utils.api_client import ( # noqa: E402
    get_tasks, get_clients, get_employees,
    create_task, update_task,
    get_tasks_by_week, format_date_es
) 

apply_responsive_css()
mobile_topbar()
back_button()

st.title("📅 Tareas y Agenda")
st.divider()

ESTADOS    = ["pendiente", "en_progreso", "completada", "cancelada"]
PRIORIDADES = ["baja", "media", "alta"]

if es_admin:
    tab_agenda, tab_lista, tab_nueva = st.tabs([
        "🗓️ Agenda semanal", "📋 Todas las tareas", "➕ Nueva tarea"
    ])
else:
    tab_agenda, tab_lista = st.tabs([
        "🗓️ Agenda semanal", "📋 Mis tareas"
    ])
    tab_nueva = None

# ── Tab: Agenda semanal ────────────────────────────────────────
with tab_agenda:
    st.subheader("Agenda semanal")

    # Inicializa semana en session_state
    if "semana_inicio" not in st.session_state:
        hoy = date.today()
        st.session_state.semana_inicio = hoy - timedelta(days=hoy.weekday())

    # Navegación
    col_nav1, col_nav2, col_nav3 = st.columns([1, 3, 1])
    with col_nav1:
        if st.button("◀ Anterior", key="prev", use_container_width=True):
            st.session_state.semana_inicio -= timedelta(weeks=1)
            st.rerun()
    with col_nav3:
        if st.button("Siguiente ▶", key="next", use_container_width=True):
            st.session_state.semana_inicio += timedelta(weeks=1)
            st.rerun()
    with col_nav2:
        inicio = st.session_state.semana_inicio
        fin    = inicio + timedelta(days=6)
        st.markdown(
            f"<div style='text-align:center; padding-top:8px;'>"
            f"📅 <b>{format_date_es(str(inicio))}</b> → "
            f"<b>{format_date_es(str(fin))}</b></div>",
            unsafe_allow_html=True
        )

    try:
        tareas_semana = get_tasks_by_week(inicio, fin)

        # Empleados solo ven sus tareas
        if not es_admin and mi_employee_id:
            tareas_semana = [
                t for t in tareas_semana
                if any(e["id"] == mi_employee_id for e in t.get("employees", []))
            ]
        dias          = [inicio + timedelta(days=i) for i in range(7)]
        nombres_dias  = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]

        cols = st.columns(7)
        for i, (col, dia) in enumerate(zip(cols, dias)):
            with col:
                es_hoy = dia == date.today()
                st.markdown(
                    f"**{'🔵 ' if es_hoy else ''}{nombres_dias[i]}**"
                )
                st.caption(format_date_es(str(dia)))
                tareas_dia = [t for t in tareas_semana if t["date"][:10] == str(dia)]
                if tareas_dia:
                    for t in tareas_dia:
                        color = "🔴" if t["priority"] == "alta" else "🟡" if t["priority"] == "media" else "🟢"
                        st.markdown(f"{color} {t['title']}")
                        if t.get("start_time"):
                            st.caption(f"🕐 {t['start_time'][:5]}")
                else:
                    st.caption("—")
    except Exception as e:
        st.error(f"Error al cargar agenda: {e}")

# ── Tab: Todas las tareas ──────────────────────────────────────
with tab_lista:
    try:
        tareas = get_tasks()

        # Empleados solo ven sus tareas asignadas
        if not es_admin and mi_employee_id:
            tareas = [
                t for t in tareas
                if any(e["id"] == mi_employee_id for e in t.get("employees", []))
            ]
        if not tareas:
            st.info("No hay tareas registradas.")
        else:
            # Filtros
            col_f1, col_f2 = st.columns(2)
            with col_f1:
                filtro_estado = st.selectbox("Filtrar por estado",
                    ["Todos"] + ESTADOS)
            with col_f2:
                filtro_prioridad = st.selectbox("Filtrar por prioridad",
                    ["Todas"] + PRIORIDADES)

            if filtro_estado != "Todos":
                tareas = [t for t in tareas if t["status"] == filtro_estado]
            if filtro_prioridad != "Todas":
                tareas = [t for t in tareas if t["priority"] == filtro_prioridad]

            st.caption(f"{len(tareas)} tareas")

            for t in tareas:
                color = "🔴" if t["priority"] == "alta" else "🟡" if t["priority"] == "media" else "🟢"
                with st.expander(f"{color} {t['title']}  —  {format_date_es(t['date'])}"):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.markdown(f"**📋 Descripción:** {t.get('description') or '—'}")
                        st.markdown(f"**📆 Fecha:** {format_date_es(t['date'])}")
                        hora_i = t.get('start_time', '')[:5] if t.get('start_time') else '—'
                        hora_f = t.get('end_time', '')[:5] if t.get('end_time') else '—'
                        st.markdown(f"**🕐 Horario:** {hora_i} → {hora_f}")
                        st.markdown(f"**📌 Estado:** {t['status']}")
                        st.markdown(f"**🔺 Prioridad:** {t['priority']}")
                        st.markdown(f"**📝 Notas:** {t.get('notes') or '—'}")

                    with col2:
                        st.markdown("**✏️ Cambiar estado**")
                        with st.form(key=f"edit_task_{t['id']}"):
                            nuevo_estado = st.selectbox("Estado", ESTADOS,
                                index=ESTADOS.index(t['status']) if t['status'] in ESTADOS else 0)
                            nueva_prioridad = st.selectbox("Prioridad", PRIORIDADES,
                                index=PRIORIDADES.index(t['priority']) if t['priority'] in PRIORIDADES else 1)
                            nuevas_notas = st.text_area("Notas", value=t.get('notes') or "")

                            col_s, col_d = st.columns(2)
                            if es_admin:
                                col_s, col_d = st.columns(2)
                                with col_s:
                                    if st.form_submit_button("💾 Guardar", use_container_width=True):
                                        try:
                                            update_task(t['id'], {
                                                "status":   nuevo_estado,
                                                "priority": nueva_prioridad,
                                                "notes":    nuevas_notas or None,
                                            })
                                            st.success("Tarea actualizada.")
                                            st.rerun()
                                        except Exception as ex:
                                            st.error(f"Error: {ex}")
                                with col_d:
                                    if st.form_submit_button("🗑️ Cancelar", use_container_width=True):
                                        try:
                                            update_task(t['id'], {"status": "cancelada"})
                                            st.warning("Tarea cancelada.")
                                            st.rerun()
                                        except Exception as ex:
                                            st.error(f"Error: {ex}")
                            else:
                                if st.form_submit_button("💾 Guardar estado", use_container_width=True):
                                    try:
                                        update_task(t['id'], {"status": nuevo_estado})
                                        st.success("Estado actualizado.")
                                        st.rerun()
                                    except Exception as ex:
                                        st.error(f"Error: {ex}")

    except Exception as e:
        st.error(f"❌ Error al cargar tareas: {e}")

# ── Tab: Nueva tarea ───────────────────────────────────────────
if tab_nueva:
    with tab_nueva:
        st.subheader("Crear nueva tarea")
        try:
            clientes  = get_clients()
            empleados = get_employees()

            clientes_opciones  = {c['name']: c['id'] for c in clientes}
            empleados_opciones = {e['name']: e['id'] for e in empleados}

            with st.form("form_nueva_tarea"):
                title       = st.text_input("Título *", placeholder="Mantenimiento jardín mensual")
                description = st.text_area("Descripción", placeholder="Detalle del trabajo a realizar...")
                col1, col2  = st.columns(2)
                with col1:
                    fecha      = st.date_input("Fecha *", value=date.today())
                    hora_inicio = st.time_input("Hora de inicio")
                    prioridad  = st.selectbox("Prioridad", PRIORIDADES, index=1)
                with col2:
                    hora_fin   = st.time_input("Hora de fin")
                    cliente    = st.selectbox("Cliente *", list(clientes_opciones.keys()))
                    estado     = st.selectbox("Estado", ESTADOS)

                empleados_sel = st.multiselect(
                    "Empleados asignados",
                    list(empleados_opciones.keys())
                )
                notas = st.text_area("Notas", placeholder="Observaciones adicionales...")

                submitted = st.form_submit_button("➕ Crear tarea", use_container_width=True)

                if submitted:
                    if not title:
                        st.error("El título es obligatorio.")
                    elif not cliente:
                        st.error("Debes seleccionar un cliente.")
                    else:
                        try:
                            create_task({
                                "title":        title,
                                "description":  description or None,
                                "date":         str(fecha),
                                "start_time":   str(hora_inicio),
                                "end_time":     str(hora_fin),
                                "status":       estado,
                                "priority":     prioridad,
                                "client_id":    clientes_opciones[cliente],
                                "employee_ids": [empleados_opciones[e] for e in empleados_sel],
                                "notes":        notas or None,
                            })
                            st.success(f"✅ Tarea '{title}' creada correctamente.")
                            st.rerun()
                        except Exception as ex:
                            st.error(f"❌ Error: {ex}")

        except Exception as e:
            st.error(f"❌ Error al cargar datos: {e}")