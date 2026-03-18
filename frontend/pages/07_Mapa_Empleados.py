"""
Página de mapa de empleados.
Muestra las tareas del día asignadas a cada empleado con urgencia por color.
Permite abrir Google Maps con la ruta propuesta al trabajo seleccionado.
"""
import sys
import os
import streamlit as st
import streamlit.components.v1 as components
from datetime import date, timedelta
import urllib.parse

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.auth import require_auth, is_admin_or_encargado, get_employee_id

st.set_page_config(page_title="Mapa Empleados · GardenManager", page_icon="🧭", layout="wide")

require_auth()

es_admin       = is_admin_or_encargado()
mi_employee_id = get_employee_id()

from utils.responsive import apply_responsive_css, mobile_topbar, back_button # noqa: E402
from utils.api_client import ( # noqa: E402
    get_employees, get_tasks_by_day, get_tasks_by_week,
    update_employee_coordinates, format_date_es
)
import folium # noqa: E402
from streamlit_folium import st_folium # noqa: E402

apply_responsive_css()
mobile_topbar()
back_button()

st.title("🧭 Mapa de empleados y rutas")
st.divider()

# ── Colores ────────────────────────────────────────────────────
COLORES_PRIORIDAD = {
    "alta":  {"marker": "red",    "hex": "#e74c3c", "emoji": "🔴"},
    "media": {"marker": "orange", "hex": "#f39c12", "emoji": "🟡"},
    "baja":  {"marker": "green",  "hex": "#27ae60", "emoji": "🟢"},
}
COLORES_EMPLEADO = ["blue", "purple", "cadetblue", "darkblue", "darkpurple", "darkred", "black"]


def google_maps_url(origin_lat, origin_lon, dest_lat, dest_lon) -> str:
    return (
        f"https://www.google.com/maps/dir/?api=1"
        f"&origin={origin_lat},{origin_lon}"
        f"&destination={dest_lat},{dest_lon}"
        f"&travelmode=driving"
    )


def google_maps_address_url(address: str) -> str:
    return f"https://www.google.com/maps/search/{urllib.parse.quote(address)}"


try:
    empleados = get_employees()

    # Empleados solo ven su propio marcador y rutas
    if not es_admin and mi_employee_id:
        empleados = [e for e in empleados if e["id"] == mi_employee_id]
    if not empleados:
        st.info("No hay empleados registrados.")
        st.stop()

    # ── GPS — lee query params ─────────────────────────────────
    params = st.query_params
    if "gps_lat" in params and "gps_lon" in params and "gps_emp" in params:
        try:
            gps_lat    = float(params["gps_lat"])
            gps_lon    = float(params["gps_lon"])
            gps_emp_id = int(params["gps_emp"])
            emp_nombre = next((e["name"] for e in empleados if e["id"] == gps_emp_id), "Empleado")
            st.success(f"📍 GPS recibido para **{emp_nombre}**: {gps_lat:.6f}, {gps_lon:.6f}")
            if st.button("💾 Guardar mi ubicación actual", use_container_width=True):
                update_employee_coordinates(gps_emp_id, gps_lat, gps_lon)
                url_params = {k: v for k, v in dict(params).items()
                              if k not in ["gps_lat", "gps_lon", "gps_emp"]}
                st.query_params.clear()
                if url_params:
                    st.query_params.update(url_params)
                st.cache_data.clear()
                st.success("✅ Ubicación guardada.")
                st.rerun()
        except Exception as ex:
            st.error(f"Error al procesar GPS: {ex}")

    # ── Selector de fecha y semana ─────────────────────────────
    col_fecha, col_semana, col_info = st.columns([2, 2, 2])
    with col_fecha:
        fecha_sel = st.date_input(
            "📅 Fecha",
            value=date.today(),
            help="Ver tareas de un día específico"
        )
    with col_semana:
        ver_semana = st.checkbox("📆 Ver semana completa", value=False)

    # ── Carga tareas según filtro ──────────────────────────────
    if ver_semana:
        inicio_sem = fecha_sel - timedelta(days=fecha_sel.weekday())
        fin_sem    = inicio_sem + timedelta(days=6)
        tareas_dia = get_tasks_by_week(inicio_sem, fin_sem)
        rango_txt  = f"{format_date_es(str(inicio_sem))} → {format_date_es(str(fin_sem))}"
    else:
        tareas_dia = get_tasks_by_day(fecha_sel)
        rango_txt  = format_date_es(str(fecha_sel))

    with col_info:
        st.markdown(f"**{rango_txt}**")
        st.caption(f"{len(tareas_dia)} tarea(s) · {len(empleados)} empleados")

    if not tareas_dia:
        st.info(f"No hay tareas para: **{rango_txt}**")

    # ── GPS — botón para obtener ubicación ────────────────────
    with st.expander("📍 Actualizar mi ubicación GPS", expanded=False):
        emp_opciones_gps = {e['name']: e for e in empleados}
        emp_gps_sel = st.selectbox(
            "Selecciona tu empleado",
            list(emp_opciones_gps.keys()),
            key="gps_emp_sel"
        )
        emp_id_sel = emp_opciones_gps[emp_gps_sel]["id"]

        gps_html = f"""
        <div style="font-family:Arial; padding:8px;">
            <div id="gps_status" style="font-size:13px; margin-bottom:8px;">
                📍 Haz clic para obtener tu ubicación actual.
            </div>
            <button onclick="getLocation()" style="
                background:#2D6A4F; color:white; border:none;
                padding:10px 20px; border-radius:6px;
                font-size:14px; cursor:pointer;
            ">📍 Obtener mi ubicación GPS</button>
            <div id="coords" style="margin-top:8px; font-size:12px; color:#2D6A4F;"></div>
        </div>
        <script>
        function getLocation() {{
            const status = document.getElementById('gps_status');
            status.innerHTML = '⏳ Obteniendo ubicación...';
            if (!navigator.geolocation) {{
                status.innerHTML = '❌ Tu navegador no soporta geolocalización.';
                return;
            }}
            navigator.geolocation.getCurrentPosition(
                function(pos) {{
                    const lat = pos.coords.latitude.toFixed(6);
                    const lon = pos.coords.longitude.toFixed(6);
                    const acc = Math.round(pos.coords.accuracy);
                    status.innerHTML = '✅ Ubicación obtenida';
                    document.getElementById('coords').innerHTML =
                        'Lat: <b>' + lat + '</b> · Lon: <b>' + lon + '</b> · Precisión: ' + acc + 'm';
                    const url = new URL(window.parent.location.href);
                    url.searchParams.set('gps_lat', lat);
                    url.searchParams.set('gps_lon', lon);
                    url.searchParams.set('gps_emp', '{emp_id_sel}');
                    window.parent.location.replace(url.toString());
                }},
                function(err) {{
                    let msg = '❌ ';
                    if (err.code === 1) msg += 'Permiso denegado.';
                    else if (err.code === 2) msg += 'Posición no disponible.';
                    else msg += 'Tiempo de espera agotado.';
                    document.getElementById('gps_status').innerHTML = msg;
                }},
                {{ enableHighAccuracy: true, timeout: 10000 }}
            );
        }}
        </script>
        """
        components.html(gps_html, height=120)

    # ── Geocodificar empleados sin coordenadas ─────────────────
    empleados_sin_coords = [e for e in empleados if not e.get("latitude")]
    if empleados_sin_coords:
        with st.spinner(f"Localizando {len(empleados_sin_coords)} empleado(s)..."):
            for i, e in enumerate(empleados_sin_coords):
                lat = 36.6937 + (i * 0.002)
                lon = -4.5246 + (i * 0.002)
                update_employee_coordinates(e["id"], lat, lon)
                e["latitude"]  = lat
                e["longitude"] = lon

# ── Filtros ────────────────────────────────────────────────
    with st.expander("🔍 Filtros", expanded=False):
        col_f1, col_f2, col_f3 = st.columns(3)

        with col_f1:
            # Filtro por empleado
            emp_nombres = ["Todos"] + [e["name"] for e in empleados]
            filtro_emp  = st.multiselect(
                "👷 Empleados",
                emp_nombres[1:],
                placeholder="Todos los empleados"
            )

        with col_f2:
            # Extrae zonas únicas de los clientes de las tareas
            zonas = sorted(set(
                t.get("client", {}).get("address", "").split(",")[-1].strip()
                for t in tareas_dia
                if t.get("client", {}).get("address")
            ))
            filtro_zona = st.multiselect(
                "📍 Zona",
                zonas,
                placeholder="Todas las zonas"
            )

        with col_f3:
            filtro_prioridad = st.multiselect(
                "🔺 Prioridad",
                ["alta", "media", "baja"],
                placeholder="Todas las prioridades"
            )

    # ── Aplica filtros ─────────────────────────────────────────
    tareas_filtradas = tareas_dia.copy()

    if filtro_emp:
        tareas_filtradas = [
            t for t in tareas_filtradas
            if any(e["name"] in filtro_emp for e in t.get("employees", []))
        ]

    if filtro_zona:
        tareas_filtradas = [
            t for t in tareas_filtradas
            if t.get("client", {}).get("address", "").split(",")[-1].strip() in filtro_zona
        ]

    if filtro_prioridad:
        tareas_filtradas = [
            t for t in tareas_filtradas
            if t.get("priority") in filtro_prioridad
        ]

    # Filtra también empleados que tienen tareas en el resultado
    if filtro_emp:
        empleados_filtrados = [e for e in empleados if e["name"] in filtro_emp]
    else:
        empleados_filtrados = empleados

    # Resumen de filtros activos
    if filtro_emp or filtro_zona or filtro_prioridad:
        st.info(
            f"🔍 Filtros activos — "
            f"{len(tareas_filtradas)} tarea(s) · "
            f"{len(empleados_filtrados)} empleado(s)"
        )

    # ── Mapa ───────────────────────────────────────────────────
    lats   = [e["latitude"]  for e in empleados if e.get("latitude")]
    lons   = [e["longitude"] for e in empleados if e.get("longitude")]
    centro = [sum(lats)/len(lats), sum(lons)/len(lons)] if lats else [36.6937, -4.5246]

    mapa = folium.Map(location=centro, zoom_start=12, tiles="OpenStreetMap")

    # Leyenda
    leyenda_html = """
    <div style="
        position:fixed; bottom:30px; left:50px; z-index:1000;
        background:rgba(255,255,255,0.97); padding:12px 18px;
        border-radius:8px; border:2px solid #2D6A4F;
        font-family:Arial; font-size:13px; color:#1B4332;
        box-shadow:0 2px 8px rgba(0,0,0,0.3);
    ">
        <b>🔺 Urgencia</b><br>
        🔴 Alta &nbsp;&nbsp; 🟡 Media &nbsp;&nbsp; 🟢 Baja<br>
        <hr style="margin:6px 0; border-color:#2D6A4F;">
        <b>📍 Marcadores</b><br>
        🔵 Empleado &nbsp;&nbsp; 🎯 Trabajo
    </div>
    """
    mapa.get_root().html.add_child(folium.Element(leyenda_html))

    # Agrupa tareas por empleado
    empleados_con_tareas = {}
    for t in tareas_filtradas:
        for emp in t.get("employees", []):
            emp_id = emp["id"]
            if emp_id not in empleados_con_tareas:
                empleados_con_tareas[emp_id] = []
            empleados_con_tareas[emp_id].append(t)

    # Marcadores de empleados
    for i, emp in enumerate(empleados_filtrados):
        if not emp.get("latitude"):
            continue

        color_emp  = COLORES_EMPLEADO[i % len(COLORES_EMPLEADO)]
        tareas_emp = empleados_con_tareas.get(emp["id"], [])

        tareas_html = "".join([
            f"<li>{COLORES_PRIORIDAD[t['priority']]['emoji']} "
            f"<b>{t['title']}</b> · "
            f"{t.get('start_time','')[:5] if t.get('start_time') else '—'}</li>"
            for t in tareas_emp
        ]) or "<li>Sin tareas en este período</li>"

        popup_emp = f"""
            <div style="font-family:Arial; min-width:200px;">
                <h4 style="margin:0; color:#1a237e;">👷 {emp['name']}</h4>
                <p style="margin:2px 0; color:#666;">{emp.get('role','')}</p>
                <hr style="margin:4px 0;">
                <b>Tareas ({len(tareas_emp)}):</b>
                <ul style="margin:4px 0; padding-left:16px;">{tareas_html}</ul>
            </div>
        """

        folium.Marker(
            location=[emp["latitude"], emp["longitude"]],
            popup=folium.Popup(popup_emp, max_width=280),
            tooltip=f"👷 {emp['name']} · {len(tareas_emp)} tarea(s)",
            icon=folium.Icon(color=color_emp, icon="user", prefix="fa")
        ).add_to(mapa)

        folium.Marker(
            location=[emp["latitude"], emp["longitude"]],
            icon=folium.DivIcon(
                html=f"""<div style="
                    font-size:11px; font-weight:bold; color:#1a237e;
                    background:rgba(255,255,255,0.88);
                    padding:2px 6px; border-radius:4px;
                    border:1px solid #3949ab; white-space:nowrap;
                    margin-top:-8px; margin-left:16px;
                ">{emp['name']}</div>""",
                icon_size=(160, 20), icon_anchor=(0, 0)
            )
        ).add_to(mapa)

        # Líneas de ruta
        for t in tareas_emp:
            cliente = t.get("client", {})
            if cliente.get("latitude") and cliente.get("longitude"):
                folium.PolyLine(
                    locations=[
                        [emp["latitude"],     emp["longitude"]],
                        [cliente["latitude"], cliente["longitude"]]
                    ],
                    color=COLORES_PRIORIDAD[t["priority"]]["hex"],
                    weight=2.5, opacity=0.7, dash_array="6 4",
                    tooltip=f"{emp['name']} → {t['title']}"
                ).add_to(mapa)

    # Marcadores de tareas/clientes
    for t in tareas_filtradas:
        cliente = t.get("client", {})
        if not cliente.get("latitude"):
            continue

        prioridad = t.get("priority", "media")
        color_t   = COLORES_PRIORIDAD[prioridad]["marker"]
        emoji_t   = COLORES_PRIORIDAD[prioridad]["emoji"]
        hora_i    = t.get("start_time", "")[:5] if t.get("start_time") else "—"
        hora_f    = t.get("end_time",   "")[:5] if t.get("end_time")   else "—"
        asignados = ", ".join(e["name"] for e in t.get("employees", [])) or "Sin asignar"

        popup_tarea = f"""
            <div style="font-family:Arial; min-width:220px;">
                <h4 style="margin:0; color:{COLORES_PRIORIDAD[prioridad]['hex']};">
                    {emoji_t} {t['title']}
                </h4>
                <hr style="margin:4px 0;">
                <p style="margin:2px 0;">📍 {cliente.get('address','—')}</p>
                <p style="margin:2px 0;">🕐 {hora_i} → {hora_f}</p>
                <p style="margin:2px 0;">👷 {asignados}</p>
                <p style="margin:2px 0;">📝 {t.get('description') or '—'}</p>
            </div>
        """

        folium.Marker(
            location=[cliente["latitude"], cliente["longitude"]],
            popup=folium.Popup(popup_tarea, max_width=280),
            tooltip=f"{emoji_t} {t['title']} · {cliente.get('name','—')}",
            icon=folium.Icon(color=color_t, icon="wrench", prefix="fa")
        ).add_to(mapa)

    # ── Layout mapa + panel ────────────────────────────────────
    col_mapa, col_panel = st.columns([3, 1])

    with col_mapa:
        st.caption(
            "🔵 Empleados · 🎯 Trabajos por urgencia · "
            "Líneas punteadas = rutas"
        )
        st_folium(mapa, height=560, use_container_width=True)

    with col_panel:
        st.subheader("📋 Tareas")
        st.caption(rango_txt)

        if not tareas_dia:
            st.info("Sin tareas en este período.")
        else:
            for prioridad in ["alta", "media", "baja"]:
                tareas_p = [t for t in tareas_filtradas if t.get("priority") == prioridad]
                if not tareas_p:
                    continue

                emoji = COLORES_PRIORIDAD[prioridad]["emoji"]
                st.markdown(f"**{emoji} {prioridad.upper()}**")

                for t in tareas_p:
                    cliente     = t.get("client", {})
                    empleados_t = [e["name"] for e in t.get("employees", [])]
                    hora_i      = t.get("start_time","")[:5] if t.get("start_time") else "—"

                    with st.container(border=True):
                        st.markdown(f"**{t['title']}**")
                        st.caption(f"🕐 {hora_i} · 📍 {cliente.get('name','—')}")
                        if empleados_t:
                            st.caption(f"👷 {', '.join(empleados_t)}")

                        dest_lat = cliente.get("latitude")
                        dest_lon = cliente.get("longitude")
                        address  = cliente.get("address", "")

                        if dest_lat and dest_lon:
                            emp_origen = next(
                                (e for e in empleados
                                 if e["id"] in [x["id"] for x in t.get("employees",[])]
                                 and e.get("latitude")),
                                None
                            )
                            url = (
                                google_maps_url(
                                    emp_origen["latitude"], emp_origen["longitude"],
                                    dest_lat, dest_lon
                                ) if emp_origen
                                else google_maps_address_url(address)
                            )
                        else:
                            url = google_maps_address_url(address) if address else None

                        if url:
                            st.link_button(
                                "🗺️ Ver ruta",
                                url,
                                use_container_width=True
                            )

except Exception as e:
    st.error(f"❌ Error al cargar el mapa de empleados: {e}")
    st.exception(e)