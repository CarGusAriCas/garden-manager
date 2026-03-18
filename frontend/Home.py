"""
Página principal de GardenManager©.
Dashboard adaptativo según dispositivo (móvil/tablet/desktop).
"""
import streamlit as st
import sys
import os

sys.path.append(os.path.dirname(__file__))

from utils.api_client import (
    get_clients, get_employees, get_tasks, get_jobs, get_absences,
    format_date_es, login, activate_account,
    request_password_reset, confirm_password_reset, ping_backend
)
from utils.responsive import apply_responsive_css, mobile_topbar, device_selector, init_device
from utils.auth import init_auth, is_authenticated, get_role, get_nombre, logout

st.set_page_config(page_title="Jardineando.es", page_icon="🌿", layout="wide")

init_auth()

# ── Lee query params para activación y reset ──────────────
params         = st.query_params
activate_token = params.get("activate")
reset_token    = params.get("reset")

# ══════════════════════════════════════════════════════════
# PANTALLA DE ACTIVACIÓN
# ══════════════════════════════════════════════════════════
if activate_token:
    st.markdown("<h1 style='text-align:center'>🌿 GardenManager</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align:center'>Activa tu cuenta</h3>", unsafe_allow_html=True)
    st.divider()
    with st.form("form_activate"):
        new_pass     = st.text_input("Nueva contraseña",    type="password", placeholder="Mínimo 8 caracteres")
        confirm_pass = st.text_input("Confirma contraseña", type="password")
        if st.form_submit_button("✅ Activar cuenta", use_container_width=True, type="primary"):
            if len(new_pass) < 8:
                st.error("La contraseña debe tener al menos 8 caracteres.")
            elif new_pass != confirm_pass:
                st.error("Las contraseñas no coinciden.")
            else:
                r = activate_account(activate_token, new_pass, confirm_pass)
                if r.get("ok"):
                    st.success("✅ Cuenta activada. Ya puedes iniciar sesión.")
                    st.query_params.clear()
                    st.rerun()
                else:
                    st.error(f"❌ {r.get('error')}")
    st.stop()

# ══════════════════════════════════════════════════════════
# PANTALLA DE RESET DE CONTRASEÑA
# ══════════════════════════════════════════════════════════
elif reset_token:
    st.markdown("<h1 style='text-align:center'>🌿 GardenManager</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align:center'>Nueva contraseña</h3>", unsafe_allow_html=True)
    st.divider()
    with st.form("form_reset"):
        new_pass     = st.text_input("Nueva contraseña",    type="password")
        confirm_pass = st.text_input("Confirma contraseña", type="password")
        if st.form_submit_button("🔑 Cambiar contraseña", use_container_width=True, type="primary"):
            if new_pass != confirm_pass:
                st.error("Las contraseñas no coinciden.")
            elif len(new_pass) < 8:
                st.error("Mínimo 8 caracteres.")
            else:
                r = confirm_password_reset(reset_token, new_pass, confirm_pass)
                if r.get("ok"):
                    st.success("✅ Contraseña cambiada. Ya puedes iniciar sesión.")
                    st.query_params.clear()
                    st.rerun()
                else:
                    st.error(f"❌ {r.get('error')}")
    st.stop()

# ══════════════════════════════════════════════════════════
# PANTALLA DE LOGIN
# ══════════════════════════════════════════════════════════
elif not is_authenticated():
    st.markdown("<h1 style='text-align:center'>🌿 GardenManager©</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:#666; font-size:1.1rem'>Sistema de gestión de jardinería</p>", unsafe_allow_html=True)
    st.divider()

    col_l, col_c, col_r = st.columns([1, 2, 1])
    with col_c:
        tab_login, tab_reset = st.tabs(["🔐 Iniciar sesión", "🔑 Olvidé mi contraseña"])

        with tab_login:
            with st.form("form_login"):
                email    = st.text_input("Email",      placeholder="tu@email.com")
                password = st.text_input("Contraseña", type="password", placeholder="Tu contraseña")
                if st.form_submit_button("Entrar →", use_container_width=True, type="primary"):
                    if not email or not password:
                        st.error("Rellena todos los campos.")
                    else:
                        with st.spinner("Verificando..."):
                            r = login(email, password)
                        if r.get("ok"):
                            st.session_state["authenticated"]        = True
                            st.session_state["token"]                = r["access_token"]
                            st.session_state["role"]                 = r["role"]
                            st.session_state["nombre"]               = r["nombre"]
                            st.session_state["employee_id"]          = r.get("employee_id")
                            st.session_state["must_change_password"] = r["must_change_password"]
                            st.rerun()
                        else:
                            st.error(f"❌ {r.get('error')}")

        with tab_reset:
            with st.form("form_forgot"):
                email_reset = st.text_input("Email", placeholder="tu@email.com", key="email_reset")
                if st.form_submit_button("📧 Enviar instrucciones", use_container_width=True):
                    if not email_reset:
                        st.error("Introduce tu email.")
                    else:
                        request_password_reset(email_reset)
                        st.info("📧 Si el email existe recibirás instrucciones en tu correo.")
    st.stop()

# ══════════════════════════════════════════════════════════
# DASHBOARD — usuario autenticado
# ══════════════════════════════════════════════════════════
apply_responsive_css()
init_device()
device_selector()
mobile_topbar()

st.components.v1.html("""
    <script>
        const width = window.innerWidth;
        let device = 'desktop';
        if (width < 768) device = 'mobile';
        else if (width < 1024) device = 'tablet';
        window.parent.postMessage({ type: 'streamlit:setComponentValue', value: device }, '*');
        localStorage.setItem('gm_device', device);
        localStorage.setItem('gm_width', width);
    </script>
""", height=0)

if "device" not in st.session_state:
    st.session_state["device"] = "desktop"

with st.sidebar:
    st.markdown("### 🌿 GardenManager©")
    st.divider()
    if st.button("📱 Notificaciones", use_container_width=True):
        st.switch_page("pages/10_Notificaciones.py")
    if st.button("💡 Enviar sugerencia", use_container_width=True):
        st.switch_page("pages/15_Sugerencias.py")
    st.caption("🔧 Simular dispositivo")
    device_override = st.selectbox(
        "Vista",
        ["auto", "desktop", "tablet", "mobile"],
        label_visibility="collapsed"
    )
    if device_override != "auto":
        st.session_state["device"] = device_override
    st.divider()
    st.caption(f"👤 {get_nombre()}")
    st.caption(f"🔑 {get_role()}")
    if st.button("🚪 Cerrar sesión", use_container_width=True):
        logout()
        st.rerun()

device = st.session_state.get("device", "desktop")

# ── Carga de datos ─────────────────────────────────────────────
with st.spinner("🌿 Conectando con el servidor..."):
    ping_backend()
    try:
        clientes  = get_clients()
        empleados = get_employees()
        tareas    = get_tasks()
        trabajos  = get_jobs()
        ausencias = get_absences()
    except Exception as e:
        st.error(f"❌ No se puede conectar con el servidor.\n\n{e}")
        st.stop()

pendientes           = [t for t in tareas   if t["status"] == "pendiente"]
urgentes             = [t for t in pendientes if t["priority"] == "alta"]
ausencias_pendientes = [a for a in ausencias if not a["is_approved"]]
en_progreso          = [j for j in trabajos  if j["status"] == "en_progreso"]
incompletos          = [j for j in trabajos  if j["status"] == "incompleto"]
incidencias          = [
    item for j in trabajos
    for item in j.get("checklist_items", [])
    if item["has_incident"]
]

def grafico_tareas_semana(tareas: list, semana_sel) -> None:
    """Gráfico de línea — evolución de tareas por día de la semana seleccionada."""
    from datetime import timedelta
    import plotly.graph_objects as go

    dias    = [semana_sel + timedelta(days=i) for i in range(7)]
    nombres = ["Lun", "Mar", "Mié", "Jue", "Vie", "Sáb", "Dom"]

    pendientes_d  = []
    completadas_d = []
    en_progreso_d = []

    for dia in dias:
        tareas_dia = [t for t in tareas if t["date"][:10] == str(dia)]
        pendientes_d.append(len([t for t in tareas_dia if t["status"] == "pendiente"]))
        completadas_d.append(len([t for t in tareas_dia if t["status"] == "completada"]))
        en_progreso_d.append(len([t for t in tareas_dia if t["status"] == "en_progreso"]))

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=nombres, y=pendientes_d,
        name="Pendientes", mode="lines+markers",
        line=dict(color="#f39c12", width=2), marker=dict(size=8)
    ))
    fig.add_trace(go.Scatter(
        x=nombres, y=en_progreso_d,
        name="En progreso", mode="lines+markers",
        line=dict(color="#3498db", width=2), marker=dict(size=8)
    ))
    fig.add_trace(go.Scatter(
        x=nombres, y=completadas_d,
        name="Completadas", mode="lines+markers",
        line=dict(color="#27ae60", width=2), marker=dict(size=8)
    ))
    fig.update_layout(
        title="📅 Tareas esta semana",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#ffffff"),
        legend=dict(orientation="h", y=-0.2),
        margin=dict(l=20, r=20, t=40, b=40),
        height=280,
        xaxis=dict(gridcolor="rgba(255,255,255,0.1)"),
        yaxis=dict(gridcolor="rgba(255,255,255,0.1)", tickformat="d", rangemode="nonnegative"),
    )
    st.plotly_chart(fig, width="stretch")


def grafico_tareas_por_empleado(tareas: list, empleados: list, semana_sel) -> None:
    """Gráfico de barras horizontales — tareas por empleado de la semana seleccionada."""
    from datetime import date, timedelta
    import plotly.graph_objects as go

    fin_sel = semana_sel + timedelta(days=6)

    tareas_semana = [
        t for t in tareas
        if semana_sel <= date.fromisoformat(t["date"][:10]) <= fin_sel
        and t["status"] != "cancelada"
    ]

    conteo = {}
    for t in tareas_semana:
        for emp in t.get("employees", []):
            nombre = emp["name"]
            conteo[nombre] = conteo.get(nombre, 0) + 1

    for emp in empleados:
        if emp["name"] not in conteo:
            conteo[emp["name"]] = 0

    ordenado = sorted(conteo.items(), key=lambda x: x[1], reverse=True)
    nombres  = [x[0].split()[0] for x in ordenado]
    valores  = [x[1] for x in ordenado]
    colores  = ["#27ae60" if v > 0 else "#555555" for v in valores]

    fig = go.Figure(go.Bar(
        x=valores, y=nombres,
        orientation="h",
        marker_color=colores,
        text=valores,
        textposition="outside",
    ))
    fig.update_layout(
        title="👷 Tareas por empleado",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#ffffff"),
        margin=dict(l=20, r=40, t=40, b=20),
        height=280,
        xaxis=dict(gridcolor="rgba(255,255,255,0.1)", tickformat="d", rangemode="nonnegative"),
        yaxis=dict(gridcolor="rgba(255,255,255,0.1)"),
    )
    st.plotly_chart(fig, width="stretch")

@st.fragment
def bloque_graficos(tareas, empleados):
    """Bloque de gráficos con selector de semana — recarga solo este fragmento."""
    from datetime import date, timedelta

    hoy   = date.today()
    lunes = hoy - timedelta(days=hoy.weekday())

    if "semana_dashboard" not in st.session_state:
        st.session_state["semana_dashboard"] = lunes

    col_prev, col_label, col_next = st.columns([1, 4, 1])
    with col_prev:
        if st.button("◀ Anterior", key="dash_prev", use_container_width=True):
            st.session_state["semana_dashboard"] -= timedelta(weeks=1)
            st.rerun(scope="fragment")
    with col_next:
        if st.button("Siguiente ▶", key="dash_next", use_container_width=True):
            st.session_state["semana_dashboard"] += timedelta(weeks=1)
            st.rerun(scope="fragment")

    semana_sel = st.session_state["semana_dashboard"]
    fin_sel    = semana_sel + timedelta(days=6)
    with col_label:
        st.markdown(
            f"<div style='text-align:center; padding-top:6px;'>"
            f"📅 <b>{semana_sel.strftime('%d/%m')} → {fin_sel.strftime('%d/%m/%Y')}</b>"
            f"</div>",
            unsafe_allow_html=True
        )

    col_g1, col_g2 = st.columns(2)
    with col_g1:
        grafico_tareas_semana(tareas, semana_sel)
    with col_g2:
        grafico_tareas_por_empleado(tareas, empleados, semana_sel)

# ══════════════════════════════════════════════════════════════
# VISTA MÓVIL
# ══════════════════════════════════════════════════════════════
if device == "mobile":

    st.markdown("## 🌿 GardenManager©")
    st.caption("Panel de control")

    if urgentes:
        st.error(f"🔴 {len(urgentes)} tarea(s) URGENTES pendientes")
    if incompletos:
        st.warning(f"⚠️ {len(incompletos)} trabajo(s) incompleto(s)")
    if ausencias_pendientes:
        st.warning(f"⏳ {len(ausencias_pendientes)} ausencia(s) por aprobar")

    st.divider()
    st.markdown("### Accesos rápidos")

    MODULOS = [
        ("👤", "Clientes",       f"{len(clientes)} activos",              "pages/01_Clientes.py"),
        ("👷", "Empleados",      f"{len(empleados)} activos",             "pages/02_Empleados.py"),
        ("📅", "Tareas",         f"{len(pendientes)} pendientes",         "pages/03_Tareas.py"),
        ("🏖️", "Ausencias",     f"{len(ausencias_pendientes)} pendientes","pages/04_Ausencias.py"),
        ("📋", "Trabajos",       f"{len(en_progreso)} en curso",          "pages/05_Trabajos.py"),
        ("🗺️", "Mapa",          "Ver clientes",                          "pages/06_Mapa.py"),
        ("🧭", "Rutas",          "Ver empleados",                         "pages/07_Mapa_Empleados.py"),
        ("📱", "Notificaciones", "WhatsApp · Telegram",                   "pages/10_Notificaciones.py"),
    ]

    for i in range(0, len(MODULOS), 2):
        col1, col2 = st.columns(2)
        for col, idx in zip([col1, col2], [i, i+1]):
            if idx < len(MODULOS):
                icon, nombre, detalle, pagina = MODULOS[idx]
                with col:
                    with st.container(border=True):
                        st.markdown(f"<div style='text-align:center; font-size:2.5rem'>{icon}</div>", unsafe_allow_html=True)
                        st.markdown(f"<div style='text-align:center; font-weight:bold'>{nombre}</div>", unsafe_allow_html=True)
                        st.markdown(f"<div style='text-align:center; font-size:0.75rem; color:#888'>{detalle}</div>", unsafe_allow_html=True)
                        if st.button("Abrir →", key=f"mob_{nombre}", use_container_width=True):
                            st.switch_page(pagina)

    st.divider()

    if urgentes:
        st.markdown("### 🔴 Tareas urgentes")
        for t in urgentes[:3]:
            with st.container(border=True):
                st.markdown(f"**{t['title']}**")
                st.caption(f"📆 {format_date_es(t['date'])}")
                if st.button("Ver →", key=f"mob_t_{t['id']}", use_container_width=True):
                    st.switch_page("pages/03_Tareas.py")

    if incidencias:
        st.markdown(f"### 🚨 Incidencias ({len(incidencias)})")
        for inc in incidencias[:2]:
            with st.container(border=True):
                st.caption(inc.get("incident_notes", "")[:100])
        if st.button("Ver todos los trabajos →", use_container_width=True, key="mob_jobs"):
            st.switch_page("pages/05_Trabajos.py")

# ══════════════════════════════════════════════════════════════
# VISTA TABLET
# ══════════════════════════════════════════════════════════════
elif device == "tablet":

    st.title("🌿 GardenManager©")
    st.caption("Panel de control · Empresa de jardinería")
    st.divider()

    bloque_graficos(tareas, empleados)

    if urgentes:
        st.error(f"🔴 {len(urgentes)} tarea(s) urgentes pendientes")
    if incompletos:
        st.warning(f"⚠️ {len(incompletos)} trabajo(s) incompleto(s)")

    col1, col2, col3 = st.columns(3)
    col1.metric("👤 Clientes",  len(clientes))
    col2.metric("👷 Empleados", len(empleados))
    col3.metric("📅 Tareas",    len(pendientes), delta="pendientes")

    col4, col5, col6 = st.columns(3)
    col4.metric("📋 Trabajos",    len(en_progreso),          delta="en curso")
    col5.metric("🏖️ Ausencias",   len(ausencias_pendientes), delta="por aprobar")
    col6.metric("🚨 Incidencias", len(incidencias))

    st.divider()
    st.markdown("### Módulos")
    cols = st.columns(4)
    MODULOS_TAB = [
        ("👤", "Clientes",       "pages/01_Clientes.py"),
        ("👷", "Empleados",      "pages/02_Empleados.py"),
        ("📅", "Tareas",         "pages/03_Tareas.py"),
        ("🏖️", "Ausencias",     "pages/04_Ausencias.py"),
        ("📋", "Trabajos",       "pages/05_Trabajos.py"),
        ("🗺️", "Mapa",          "pages/06_Mapa.py"),
        ("🧭", "Rutas",          "pages/07_Mapa_Empleados.py"),
        ("📱", "Notificaciones", "pages/10_Notificaciones.py"),
    ]
    for i, (icon, nombre, pagina) in enumerate(MODULOS_TAB):
        with cols[i % 4]:
            with st.container(border=True):
                st.markdown(f"<div style='text-align:center;font-size:2rem'>{icon}</div>", unsafe_allow_html=True)
                st.markdown(f"<div style='text-align:center;font-weight:bold'>{nombre}</div>", unsafe_allow_html=True)
                if st.button("Abrir", key=f"tab_{nombre}", use_container_width=True):
                    st.switch_page(pagina)

    st.divider()

    col_izq, col_der = st.columns(2)
    with col_izq:
        st.subheader("📅 Tareas pendientes")
        for t in pendientes[:4]:
            color = "🔴" if t["priority"] == "alta" else "🟡" if t["priority"] == "media" else "🟢"
            with st.container(border=True):
                col_a, col_b = st.columns([4, 1])
                with col_a:
                    st.markdown(f"{color} **{t['title']}**")
                    st.caption(f"📆 {format_date_es(t['date'])}")
                with col_b:
                    if st.button("→", key=f"tab_t_{t['id']}", use_container_width=True):
                        st.switch_page("pages/03_Tareas.py")

    with col_der:
        st.subheader("🏖️ Ausencias pendientes")
        if ausencias_pendientes:
            for a in ausencias_pendientes[:4]:
                nombre = a.get("employee", {}).get("name", "—")
                with st.container(border=True):
                    col_a, col_b = st.columns([4, 1])
                    with col_a:
                        st.markdown(f"**{nombre}**")
                        st.caption(f"📅 {format_date_es(str(a['start_date']))} → {format_date_es(str(a['end_date']))}")
                    with col_b:
                        if st.button("→", key=f"tab_a_{a['id']}", use_container_width=True):
                            st.switch_page("pages/04_Ausencias.py")
        else:
            st.success("✅ Sin ausencias pendientes.")

# ══════════════════════════════════════════════════════════════
# VISTA DESKTOP
# ══════════════════════════════════════════════════════════════
else:
    st.title("🌿 GardenManager©")
    st.caption("Panel de control · Empresa de jardinería")
    st.divider()

    bloque_graficos(tareas, empleados)

    if urgentes:
        st.error(f"🔴 {len(urgentes)} tarea(s) urgentes pendientes")
    if incompletos:
        st.warning(f"⚠️ {len(incompletos)} trabajo(s) incompleto(s)")

    st.subheader("📊 Resumen general")
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    col1.metric("👤 Clientes",    len(clientes))
    col2.metric("👷 Empleados",   len(empleados))
    col3.metric("📅 Tareas",      len(pendientes),          delta="pendientes")
    col4.metric("📋 Trabajos",    len(en_progreso),         delta="en curso")
    col5.metric("🏖️ Ausencias",   len(ausencias_pendientes),delta="por aprobar")
    col6.metric("🚨 Incidencias", len(incidencias))

    st.divider()
    bc1, bc2, bc3, bc4, bc5, bc6, bc7, bc8 = st.columns(8)
    if bc1.button("👤 Clientes",       use_container_width=True): 
        st.switch_page("pages/01_Clientes.py")
    if bc2.button("👷 Empleados",      use_container_width=True): 
        st.switch_page("pages/02_Empleados.py")
    if bc3.button("📅 Tareas",         use_container_width=True): 
        st.switch_page("pages/03_Tareas.py")
    if bc4.button("🏖️ Ausencias",      use_container_width=True): 
        st.switch_page("pages/04_Ausencias.py")
    if bc5.button("📋 Trabajos",       use_container_width=True): 
        st.switch_page("pages/05_Trabajos.py")
    if bc6.button("🗺️ Mapa clientes",  use_container_width=True): 
        st.switch_page("pages/06_Mapa.py")
    if bc7.button("🧭 Rutas",          use_container_width=True): 
        st.switch_page("pages/07_Mapa_Empleados.py")
    if bc8.button("📱 Notificaciones", use_container_width=True): 
        st.switch_page("pages/10_Notificaciones.py")

    st.divider()

    col_izq, col_centro, col_der = st.columns(3)

    with col_izq:
        st.subheader("📅 Tareas pendientes")
        for t in pendientes[:6]:
            color = "🔴" if t["priority"] == "alta" else "🟡" if t["priority"] == "media" else "🟢"
            with st.container(border=True):
                col_a, col_b = st.columns([4, 1])
                with col_a:
                    st.markdown(f"{color} **{t['title']}**")
                    cliente_nombre = t.get("client", {}).get("name", "—") if isinstance(t.get("client"), dict) else "—"
                    st.caption(f"📆 {format_date_es(t['date'])} · 👤 {cliente_nombre}")
                with col_b:
                    if st.button("→", key=f"dt_{t['id']}", use_container_width=True):
                        st.switch_page("pages/03_Tareas.py")
        if len(pendientes) > 6:
            if st.button(f"Ver {len(pendientes)-6} más →", use_container_width=True, key="mas_t"):
                st.switch_page("pages/03_Tareas.py")

    with col_centro:
        st.subheader("📋 Trabajos activos")
        activos = en_progreso + incompletos
        for j in activos[:4]:
            estado_icon = "🟡" if j["status"] == "en_progreso" else "🔴"
            n_items  = len(j.get("checklist_items", []))
            n_hechos = len([i for i in j.get("checklist_items", []) if i["is_done"]])
            n_incid  = len([i for i in j.get("checklist_items", []) if i["has_incident"]])
            with st.container(border=True):
                col_a, col_b = st.columns([4, 1])
                with col_a:
                    st.markdown(f"{estado_icon} **Trabajo #{j['id']}**")
                    st.caption(f"✅ {n_hechos}/{n_items} · 🚨 {n_incid} incidencia(s)")
                with col_b:
                    if st.button("→", key=f"dj_{j['id']}", use_container_width=True):
                        st.switch_page("pages/05_Trabajos.py")

        st.markdown("---")
        st.markdown("**🚨 Incidencias recientes**")
        for inc in incidencias[:3]:
            with st.container(border=True):
                st.caption(inc.get("incident_notes", "")[:80])
        if not incidencias:
            st.success("✅ Sin incidencias.")

    with col_der:
        st.subheader("🏖️ Ausencias pendientes")
        if ausencias_pendientes:
            for a in ausencias_pendientes[:5]:
                nombre = a.get("employee", {}).get("name", "—")
                with st.container(border=True):
                    col_a, col_b = st.columns([4, 1])
                    with col_a:
                        st.markdown(f"**{nombre}**")
                        st.caption(f"📅 {format_date_es(str(a['start_date']))} → {format_date_es(str(a['end_date']))}")
                        st.caption(f"🏷️ {a['absence_type']}")
                    with col_b:
                        if st.button("→", key=f"da_{a['id']}", use_container_width=True):
                            st.switch_page("pages/04_Ausencias.py")
        else:
            st.success("✅ Sin ausencias pendientes.")

        st.markdown("---")
        st.subheader("👤 Últimos clientes")
        ultimos = clientes[-3:] if len(clientes) >= 3 else clientes
        for c in reversed(ultimos):
            with st.container(border=True):
                col_a, col_b = st.columns([4, 1])
                with col_a:
                    st.markdown(f"**{c['name']}**")
                    st.caption(c.get("address", "—"))
                with col_b:
                    if st.button("→", key=f"dc_{c['id']}", use_container_width=True):
                        st.switch_page("pages/01_Clientes.py")