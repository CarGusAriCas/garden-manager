"""
Panel de notificaciones — WhatsApp y Telegram.
"""
import sys
import os
import streamlit as st
import urllib.parse

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.responsive import apply_responsive_css, mobile_topbar, back_button
from utils.api_client import get_employees, get_clients, get_tasks, get_absences, _post, format_date_es

apply_responsive_css()
mobile_topbar()
back_button()

st.set_page_config(
    page_title="Notificaciones · GardenManager",
    page_icon="📱",
    layout="wide"
)
st.title("📱 Notificaciones")
st.caption("Envío de mensajes via WhatsApp y Telegram")
st.divider()

tab_test, tab_libre, tab_tarea, tab_recordatorio, tab_ausencia, tab_trabajo = st.tabs([
    "🔧 Pruebas de conexión",
    "✉️ Mensaje libre",
    "📅 Tarea asignada",
    "⏰ Recordatorio",
    "🏖️ Ausencia",
    "📋 Trabajo completado",
])

# ── Tab: Pruebas ───────────────────────────────────────────────
with tab_test:
    st.subheader("Verificar conexiones")
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**📱 Test Telegram**")
        st.caption("Envía un mensaje de prueba al chat configurado en .env")
        if st.button("🤖 Probar Telegram", use_container_width=True):
            with st.spinner("Enviando..."):
                try:
                    r = _post("/notifications/test-telegram", {})
                    if r.get("ok"):
                        st.success("✅ Telegram funcionando. Revisa tu bot.")
                    else:
                        st.error(f"❌ Error: {r}")
                except Exception as e:
                    st.error(f"❌ {e}")

    with col2:
        st.markdown("**💬 Test WhatsApp**")
        st.caption("Envía un mensaje de prueba a un número del sandbox")
        numero_test = st.text_input(
            "Número destino",
            placeholder="+34612345678",
            help="Debe estar registrado en el sandbox de Twilio"
        )
        if st.button("💬 Probar WhatsApp", use_container_width=True):
            if not numero_test:
                st.error("Introduce un número.")
            else:
                with st.spinner("Enviando..."):
                    try:
                        numero_encoded = urllib.parse.quote(numero_test)
                        r = _post(f"/notifications/test-whatsapp?numero={numero_encoded}", {})
                        if r.get("ok"):
                            st.success("✅ WhatsApp funcionando. Revisa tu móvil.")
                        else:
                            st.error(f"❌ Error: {r}")
                    except Exception as e:
                        st.error(f"❌ {e}")

# ── Tab: Mensaje libre ─────────────────────────────────────────
with tab_libre:
    st.subheader("Enviar mensaje libre")

    try:
        empleados = get_employees()
        clientes  = get_clients()
        todos     = (
            [{"tipo": "empleado", **e} for e in empleados] +
            [{"tipo": "cliente",  **c} for c in clientes]
        )
        opciones = {
            f"{'👷' if p['tipo']=='empleado' else '👤'} {p['name']}": p
            for p in todos
        }

        with st.form("form_mensaje_libre"):
            destinatario_sel = st.selectbox("Destinatario", list(opciones.keys()))
            canal = st.multiselect(
                "Canal",
                ["WhatsApp", "Telegram"],
                default=["Telegram"]
            )
            mensaje = st.text_area(
                "Mensaje *",
                placeholder="Escribe tu mensaje aquí...",
                height=120
            )

            if st.form_submit_button("📤 Enviar", use_container_width=True):
                if not mensaje:
                    st.error("El mensaje es obligatorio.")
                else:
                    persona = opciones[destinatario_sel]
                    payload = {
                        "mensaje": mensaje,
                        "destinatario_whatsapp": persona.get("whatsapp_number") if "WhatsApp" in canal else None,
                        "destinatario_telegram": persona.get("telegram_chat_id") if "Telegram" in canal else None,
                    }

                    if not payload["destinatario_whatsapp"] and not payload["destinatario_telegram"]:
                        st.warning(
                            f"⚠️ {persona['name']} no tiene WhatsApp ni Telegram configurado. "
                            f"Edita su perfil en la página correspondiente."
                        )
                    else:
                        with st.spinner("Enviando..."):
                            try:
                                r = _post("/notifications/mensaje-libre", payload)
                                st.success("✅ Mensaje enviado.")
                                st.json(r)
                            except Exception as e:
                                st.error(f"❌ {e}")

    except Exception as e:
        st.error(f"❌ Error: {e}")

# ── Tab: Tarea asignada ────────────────────────────────────────
with tab_tarea:
    st.subheader("Notificar tarea asignada")

    try:
        empleados = get_employees()
        tareas    = get_tasks()

        emp_opciones   = {e['name']: e for e in empleados}
        tarea_opciones = {
            f"#{t['id']} {t['title']} ({format_date_es(t['date'])})": t
            for t in tareas
        }

        with st.form("form_notif_tarea"):
            emp_sel   = st.selectbox("Empleado", list(emp_opciones.keys()))
            tarea_sel = st.selectbox("Tarea", list(tarea_opciones.keys()))
            urgente   = st.checkbox("🔴 Marcar como urgente")
            canal     = st.multiselect("Canal", ["WhatsApp", "Telegram"], default=["Telegram"])

            if st.form_submit_button("📤 Enviar notificación", use_container_width=True):
                emp   = emp_opciones[emp_sel]
                tarea = tarea_opciones[tarea_sel]
                cliente = tarea.get("client", {})

                payload = {
                    "empleado_nombre":   emp["name"],
                    "empleado_whatsapp": emp.get("whatsapp_number") if "WhatsApp" in canal else None,
                    "empleado_telegram": emp.get("telegram_chat_id") if "Telegram" in canal else None,
                    "tarea_titulo":      tarea["title"],
                    "fecha":             format_date_es(tarea["date"]),
                    "hora":              tarea.get("start_time", "09:00")[:5] if tarea.get("start_time") else "09:00",
                    "direccion":         cliente.get("address", ""),
                    "urgente":           urgente,
                }

                if not payload["empleado_whatsapp"] and not payload["empleado_telegram"]:
                    st.warning(f"⚠️ {emp['name']} no tiene canales configurados.")
                else:
                    with st.spinner("Enviando..."):
                        try:
                            r = _post("/notifications/tarea-asignada", payload)
                            st.success("✅ Notificación enviada.")
                            st.json(r)
                        except Exception as e:
                            st.error(f"❌ {e}")

    except Exception as e:
        st.error(f"❌ Error: {e}")

# ── Tab: Recordatorio ──────────────────────────────────────────
with tab_recordatorio:
    st.subheader("Enviar recordatorio de tareas")
    st.caption("Recuerda al empleado las tareas que tiene mañana.")

    try:
        from datetime import date, timedelta
        empleados = get_employees()
        tareas    = get_tasks()

        emp_opciones = {e['name']: e for e in empleados}

        with st.form("form_recordatorio"):
            emp_sel = st.selectbox("Empleado", list(emp_opciones.keys()))

            manana  = date.today() + timedelta(days=1)
            fecha   = st.date_input("Fecha del recordatorio", value=manana)

            # Filtra tareas del empleado seleccionado en esa fecha
            emp     = emp_opciones[emp_sel]
            tareas_emp = [
                t for t in tareas
                if t["date"] == str(fecha)
                and any(e["id"] == emp["id"] for e in t.get("employees", []))
            ]

            if tareas_emp:
                st.info(f"📅 {len(tareas_emp)} tarea(s) encontradas para esa fecha:")
                for t in tareas_emp:
                    hora = t.get("start_time", "")[:5] if t.get("start_time") else "—"
                    st.caption(f"• {t['title']} · {hora}")
                tareas_titulos = [t["title"] for t in tareas_emp]
            else:
                st.warning("No hay tareas asignadas a este empleado en esa fecha.")
                tareas_titulos = []

            canal = st.multiselect("Canal", ["WhatsApp", "Telegram"], default=["Telegram"])

            if st.form_submit_button("⏰ Enviar recordatorio", use_container_width=True):
                if not tareas_titulos:
                    st.error("No hay tareas para recordar en esa fecha.")
                else:
                    payload = {
                        "empleado_nombre":   emp["name"],
                        "empleado_whatsapp": emp.get("whatsapp_number") if "WhatsApp" in canal else None,
                        "empleado_telegram": emp.get("telegram_chat_id") if "Telegram" in canal else None,
                        "tareas":            tareas_titulos,
                        "fecha":             format_date_es(str(fecha)),
                    }

                    if not payload["empleado_whatsapp"] and not payload["empleado_telegram"]:
                        st.warning(f"⚠️ {emp['name']} no tiene canales configurados.")
                    else:
                        with st.spinner("Enviando..."):
                            try:
                                r = _post("/notifications/recordatorio", payload)
                                st.success("✅ Recordatorio enviado.")
                                st.json(r)
                            except Exception as e:
                                st.error(f"❌ {e}")

    except Exception as e:
        st.error(f"❌ Error: {e}")

# ── Tab: Ausencia ──────────────────────────────────────────────
with tab_ausencia:
    st.subheader("Notificar resultado de ausencia")

    try:
        ausencias = get_absences()
        pendientes = [a for a in ausencias if not a["is_approved"]]

        if not pendientes:
            st.info("No hay ausencias pendientes de aprobación.")
        else:
            ausencia_opciones = {
                f"{a.get('employee',{}).get('name','—')} · "
                f"{format_date_es(str(a['start_date']))} → "
                f"{format_date_es(str(a['end_date']))}": a
                for a in pendientes
            }

            with st.form("form_notif_ausencia"):
                aus_sel  = st.selectbox("Ausencia pendiente", list(ausencia_opciones.keys()))
                aprobada = st.radio("Decisión", ["✅ Aprobar", "❌ Denegar"])
                motivo   = st.text_input("Motivo (opcional)", placeholder="Solo necesario si se deniega")
                canal    = st.multiselect("Canal", ["WhatsApp", "Telegram"], default=["Telegram"])

                if st.form_submit_button("📤 Notificar decisión", use_container_width=True):
                    aus = ausencia_opciones[aus_sel]
                    emp = aus.get("employee", {})

                    payload = {
                        "empleado_nombre":   emp.get("name", ""),
                        "empleado_whatsapp": emp.get("whatsapp_number") if "WhatsApp" in canal else None,
                        "empleado_telegram": emp.get("telegram_chat_id") if "Telegram" in canal else None,
                        "inicio":            format_date_es(str(aus["start_date"])),
                        "fin":               format_date_es(str(aus["end_date"])),
                        "aprobada":          aprobada == "✅ Aprobar",
                        "motivo":            motivo or "",
                    }

                    with st.spinner("Enviando..."):
                        try:
                            r = _post("/notifications/ausencia", payload)
                            st.success("✅ Notificación enviada.")
                            st.json(r)
                        except Exception as e:
                            st.error(f"❌ {e}")

    except Exception as e:
        st.error(f"❌ Error: {e}")

# ── Tab: Trabajo completado ────────────────────────────────────
with tab_trabajo:
    st.subheader("Notificar trabajo completado al cliente")

    try:
        from utils.api_client import get_jobs
        trabajos  = get_jobs()
        completados = [j for j in trabajos if j["status"] == "completado"]

        if not completados:
            st.info("No hay trabajos completados.")
        else:
            clientes  = get_clients()
            tareas    = get_tasks()
            cli_map   = {c["id"]: c for c in clientes}
            tar_map   = {t["id"]: t for t in tareas}

            trabajo_opciones = {
                f"Trabajo #{j['id']} · Tarea #{j['task_id']}": j
                for j in completados
            }

            with st.form("form_notif_trabajo"):
                job_sel = st.selectbox("Trabajo completado", list(trabajo_opciones.keys()))

                if st.form_submit_button("📤 Notificar al cliente", use_container_width=True):
                    job   = trabajo_opciones[job_sel]
                    tarea = tar_map.get(job["task_id"], {})
                    cli   = cli_map.get(tarea.get("client_id"), {})

                    if not cli:
                        st.error("No se encontró el cliente asociado.")
                    else:
                        payload = {
                            "cliente_nombre":   cli.get("name", ""),
                            "cliente_whatsapp": cli.get("whatsapp_number"),
                            "tarea_titulo":     tarea.get("title", ""),
                            "fecha":            format_date_es(tarea.get("date", "")),
                        }

                        if not payload["cliente_whatsapp"]:
                            st.warning(f"⚠️ {cli['name']} no tiene WhatsApp configurado.")
                        else:
                            with st.spinner("Enviando..."):
                                try:
                                    r = _post("/notifications/trabajo-completado", payload)
                                    st.success("✅ Cliente notificado.")
                                    st.json(r)
                                except Exception as e:
                                    st.error(f"❌ {e}")

    except Exception as e:
        st.error(f"❌ Error: {e}")