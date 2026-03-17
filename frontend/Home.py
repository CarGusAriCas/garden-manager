"""
Página principal de GardenManager©.
Dashboard adaptativo según dispositivo (móvil/tablet/desktop).
"""
import streamlit as st
import sys
import os

sys.path.append(os.path.dirname(__file__))

from utils.api_client import get_clients, get_employees, get_tasks, get_jobs, get_absences, format_date_es
from utils.responsive import apply_responsive_css, mobile_topbar, device_selector, init_device

st.set_page_config(
    page_title="Jardineando.es",
    page_icon="🌿",
    layout="wide"
)

apply_responsive_css()
init_device()          # ← solo en Home.py, detecta el dispositivo
device_selector()      # ← selector en sidebar
mobile_topbar()        # ← topbar si es móvil

# ── Detecta dispositivo via JS ─────────────────────────────────
st.components.v1.html("""
    <script>
        const width = window.innerWidth;
        let device = 'desktop';
        if (width < 768) device = 'mobile';
        else if (width < 1024) device = 'tablet';
        window.parent.postMessage({ type: 'streamlit:setComponentValue', value: device }, '*');

        // Escribe en un input oculto para que Streamlit lo lea
        const input = window.parent.document.querySelector('input[data-testid="stNumberInput"]');
        localStorage.setItem('gm_device', device);
        localStorage.setItem('gm_width', width);
    </script>
""", height=0)

# Detecta ancho via query param o session state
if "device" not in st.session_state:
    # Por defecto desktop — el usuario puede forzarlo
    st.session_state["device"] = "desktop"

# ── Override manual (útil para pruebas) ───────────────────────
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

device = st.session_state.get("device", "desktop")

# ── Carga de datos ─────────────────────────────────────────────
try:
    clientes  = get_clients()
    empleados = get_employees()
    tareas    = get_tasks()
    trabajos  = get_jobs()
    ausencias = get_absences()
except Exception as e:
    st.error(f"❌ No se puede conectar con el servidor.\n\n{e}")
    st.stop()

pendientes          = [t for t in tareas    if t["status"] == "pendiente"]
urgentes            = [t for t in pendientes if t["priority"] == "alta"]
ausencias_pendientes = [a for a in ausencias if not a["is_approved"]]
en_progreso         = [j for j in trabajos  if j["status"] == "en_progreso"]
incompletos         = [j for j in trabajos  if j["status"] == "incompleto"]
incidencias         = [
    item for j in trabajos
    for item in j.get("checklist_items", [])
    if item["has_incident"]
]

# ══════════════════════════════════════════════════════════════
# VISTA MÓVIL
# ══════════════════════════════════════════════════════════════
if device == "mobile":

    st.markdown("## 🌿 GardenManager©")
    st.caption("Panel de control")

    # Alertas urgentes primero
    if urgentes:
        st.error(f"🔴 {len(urgentes)} tarea(s) URGENTES pendientes")
    if incompletos:
        st.warning(f"⚠️ {len(incompletos)} trabajo(s) incompleto(s)")
    if ausencias_pendientes:
        st.warning(f"⏳ {len(ausencias_pendientes)} ausencia(s) por aprobar")

    st.divider()

    # ── Accesos rápidos con iconos grandes ────────────────────
    st.markdown("### Accesos rápidos")

    MODULOS = [
        ("👤", "Clientes",   f"{len(clientes)} activos",     "pages/01_Clientes.py"),
        ("👷", "Empleados",  f"{len(empleados)} activos",    "pages/02_Empleados.py"),
        ("📅", "Tareas",     f"{len(pendientes)} pendientes","pages/03_Tareas.py"),
        ("🏖️","Ausencias",  f"{len(ausencias_pendientes)} pendientes","pages/04_Ausencias.py"),
        ("📋", "Trabajos",   f"{len(en_progreso)} en curso", "pages/05_Trabajos.py"),
        ("🗺️", "Mapa",      "Ver clientes",                 "pages/06_Mapa.py"),
        ("🧭", "Rutas",     "Ver empleados",                "pages/07_Mapa_Empleados.py"),
        ("📱", "Notificaciones", "WhatsApp · Telegram",     "pages/10_Notificaciones.py"),  # ← AÑADE
    ]

    # Grid 2 columnas para móvil
    for i in range(0, len(MODULOS), 2):
        col1, col2 = st.columns(2)
        for col, idx in zip([col1, col2], [i, i+1]):
            if idx < len(MODULOS):
                icon, nombre, detalle, pagina = MODULOS[idx]
                with col:
                    with st.container(border=True):
                        st.markdown(
                            f"<div style='text-align:center; font-size:2.5rem'>{icon}</div>",
                            unsafe_allow_html=True
                        )
                        st.markdown(
                            f"<div style='text-align:center; font-weight:bold'>{nombre}</div>",
                            unsafe_allow_html=True
                        )
                        st.markdown(
                            f"<div style='text-align:center; font-size:0.75rem; color:#888'>{detalle}</div>",
                            unsafe_allow_html=True
                        )
                        if st.button("Abrir →", key=f"mob_{nombre}", use_container_width=True):
                            st.switch_page(pagina)

    st.divider()

    # ── Tareas urgentes en móvil ───────────────────────────────
    if urgentes:
        st.markdown("### 🔴 Tareas urgentes")
        for t in urgentes[:3]:
            with st.container(border=True):
                st.markdown(f"**{t['title']}**")
                st.caption(f"📆 {format_date_es(t['date'])}")
                if st.button("Ver →", key=f"mob_t_{t['id']}", use_container_width=True):
                    st.switch_page("pages/03_Tareas.py")

    # ── Incidencias en móvil ───────────────────────────────────
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

    # Alertas
    if urgentes:
        st.error(f"🔴 {len(urgentes)} tarea(s) de prioridad ALTA pendientes")
    if incompletos:
        st.warning(f"⚠️ {len(incompletos)} trabajo(s) incompleto(s)")

    # Métricas en 2 filas de 3
    col1, col2, col3 = st.columns(3)
    col1.metric("👤 Clientes",  len(clientes))
    col2.metric("👷 Empleados", len(empleados))
    col3.metric("📅 Tareas",    len(pendientes), delta="pendientes")

    col4, col5, col6 = st.columns(3)
    col4.metric("📋 Trabajos",  len(en_progreso), delta="en curso")
    col5.metric("🏖️ Ausencias", len(ausencias_pendientes), delta="por aprobar")
    col6.metric("🚨 Incidencias", len(incidencias))

    st.divider()

    # Accesos rápidos
    st.markdown("### Módulos")
    cols = st.columns(4)
    MODULOS_TAB = [
        ("👤", "Clientes",  "pages/01_Clientes.py"),
        ("👷", "Empleados", "pages/02_Empleados.py"),
        ("📅", "Tareas",    "pages/03_Tareas.py"),
        ("🏖️","Ausencias", "pages/04_Ausencias.py"),
        ("📋", "Trabajos",  "pages/05_Trabajos.py"),
        ("🗺️", "Mapa",     "pages/06_Mapa.py"),
        ("🧭", "Rutas",    "pages/07_Mapa_Empleados.py"),
        ("📱", "Notificaciones", "pages/10_Notificaciones.py"),  # ← AÑADE
    ]
    for i, (icon, nombre, pagina) in enumerate(MODULOS_TAB):
        with cols[i % 4]:
            with st.container(border=True):
                st.markdown(f"<div style='text-align:center;font-size:2rem'>{icon}</div>", unsafe_allow_html=True)
                st.markdown(f"<div style='text-align:center;font-weight:bold'>{nombre}</div>", unsafe_allow_html=True)
                if st.button("Abrir", key=f"tab_{nombre}", use_container_width=True):
                    st.switch_page(pagina)

    st.divider()

    # Tareas + Ausencias
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

    # Alertas
    if urgentes:
        st.error(f"🔴 {len(urgentes)} tarea(s) de prioridad ALTA pendientes")
    if incompletos:
        st.warning(f"⚠️ {len(incompletos)} trabajo(s) incompleto(s) — requieren atención")

    # Métricas
    st.subheader("📊 Resumen general")
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    col1.metric("👤 Clientes",    len(clientes))
    col2.metric("👷 Empleados",   len(empleados))
    col3.metric("📅 Tareas",      len(pendientes),          delta="pendientes")
    col4.metric("📋 Trabajos",    len(en_progreso),         delta="en curso")
    col5.metric("🏖️ Ausencias",   len(ausencias_pendientes),delta="por aprobar")
    col6.metric("🚨 Incidencias", len(incidencias))

    # Botones de módulos
    st.divider()
    bc1, bc2, bc3, bc4, bc5, bc6, bc7, bc8 = st.columns(8)
    if bc1.button("👤 Clientes",  use_container_width=True): 
        st.switch_page("pages/01_Clientes.py")
    if bc2.button("👷 Empleados", use_container_width=True): 
        st.switch_page("pages/02_Empleados.py")
    if bc3.button("📅 Tareas",    use_container_width=True): 
        st.switch_page("pages/03_Tareas.py")
    if bc4.button("🏖️ Ausencias", use_container_width=True): 
        st.switch_page("pages/04_Ausencias.py")
    if bc5.button("📋 Trabajos",  use_container_width=True): 
        st.switch_page("pages/05_Trabajos.py")
    if bc6.button("🗺️ Clientes",  use_container_width=True): 
        st.switch_page("pages/06_Mapa.py")
    if bc7.button("🧭 Rutas",     use_container_width=True): 
        st.switch_page("pages/07_Mapa_Empleados.py")
    if bc8.button("📱 Notificaciones", use_container_width=True): 
        st.switch_page("pages/10_Notificaciones.py")

    st.divider()

    # Tres columnas principales
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