"""
Página de mapa de empleados.
Muestra las tareas del día asignadas a cada empleado con urgencia por color.
Permite abrir Google Maps con la ruta propuesta al trabajo seleccionado.
"""
import streamlit as st
import sys
import os
from utils.responsive import apply_responsive_css, mobile_topbar, back_button
from datetime import date, timedelta
from utils.api_client import (
    get_employees, get_tasks_by_day, get_tasks_by_week,
    update_employee_coordinates,
    format_date_es
)
import folium
from streamlit_folium import st_folium

apply_responsive_css()
mobile_topbar()
back_button()

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

st.set_page_config(
    page_title="Mapa Empleados · GardenManager",
    page_icon="🧭",
    layout="wide"
)
st.title("🧭 Mapa de empleados y rutas")
st.divider()

# ── Colores por prioridad/urgencia ─────────────────────────────
COLORES_PRIORIDAD = {
    "alta":   {"marker": "red",    "hex": "#e74c3c", "emoji": "🔴"},
    "media":  {"marker": "orange", "hex": "#f39c12", "emoji": "🟡"},
    "baja":   {"marker": "green",  "hex": "#27ae60", "emoji": "🟢"},
}

COLORES_EMPLEADO = [
    "blue", "purple", "cadetblue", "darkblue",
    "darkpurple", "darkred", "black"
]


def google_maps_url(origin_lat, origin_lon, dest_lat, dest_lon) -> str:
    """
    Genera una URL de Google Maps con ruta desde origen hasta destino.
    No requiere API key — abre directamente la aplicación.
    """
    return (
        f"https://www.google.com/maps/dir/?api=1"
        f"&origin={origin_lat},{origin_lon}"
        f"&destination={dest_lat},{dest_lon}"
        f"&travelmode=driving"
    )


def google_maps_address_url(address: str) -> str:
    """
    Genera URL de Google Maps a partir de una dirección de texto.
    Usado cuando no hay coordenadas del empleado disponibles.
    """
    import urllib.parse
    return f"https://www.google.com/maps/search/{urllib.parse.quote(address)}"


try:
    empleados = get_employees()
    if not empleados:
        st.info("No hay empleados registrados.")
        st.stop()

    # ── Selector de fecha y semana ─────────────────────────────────
    col_fecha, col_semana, col_info = st.columns([2, 2, 2])
    with col_fecha:
        fecha_sel = st.date_input(
            "📅 Fecha concreta",
            value=date.today(),
            help="Ver tareas de un día específico"
        )

    with col_semana:
        ver_semana = st.checkbox("📆 Ver semana completa", value=False)

# Determina el rango de fechas a mostrar
    if ver_semana:
        inicio_sem  = fecha_sel - timedelta(days=fecha_sel.weekday())
        fin_sem     = inicio_sem + timedelta(days=6)
        tareas_dia  = get_tasks_by_week(inicio_sem, fin_sem)
        rango_txt   = f"{format_date_es(str(inicio_sem))} → {format_date_es(str(fin_sem))}"
    else:
        tareas_dia  = get_tasks_by_day(fecha_sel)
        rango_txt   = format_date_es(str(fecha_sel))

    with col_info:
        st.markdown(f"**{rango_txt}**")
        st.caption(f"{len(tareas_dia)} tarea(s) · {len(empleados)} empleados")

    # ── Cargar tareas del día ──────────────────────────────────
    tareas_dia = get_tasks_by_day(fecha_sel)

    with col_info:
        st.markdown(f"**{format_date_es(str(fecha_sel))}**")
        st.caption(f"{len(tareas_dia)} tarea(s) programadas · "
                   f"{len(empleados)} empleados activos")

    if not tareas_dia:
        st.warning(f"No hay tareas para: {rango_txt}")
    else:
        st.success(f"✅ {len(tareas_dia)} tarea(s) encontradas")

    # ── Geocodificar empleados sin coordenadas ─────────────────
    empleados_sin_coords = [
        e for e in empleados
        if not e.get("latitude")
    ]
    if empleados_sin_coords:
        with st.spinner(f"Localizando {len(empleados_sin_coords)} empleado(s)..."):
            for e in empleados_sin_coords:
                # Usamos Madrid centro como base para empleados sin dirección
                lat, lon = 36.6937, -4.5246
                update_employee_coordinates(e["id"], lat, lon)
                e["latitude"]  = lat
                e["longitude"] = lon

    # ── Mapa base centrado en media de coordenadas ─────────────
    lats = [e["latitude"]  for e in empleados if e.get("latitude")]
    lons = [e["longitude"] for e in empleados if e.get("longitude")]
    centro = [sum(lats)/len(lats), sum(lons)/len(lons)] if lats else [36.6937, -4.5246]

    mapa = folium.Map(location=centro, zoom_start=12, tiles="OpenStreetMap")

    # ── Leyenda de urgencia ────────────────────────────────────
    leyenda_html = """
    <div style="
        position: fixed; bottom: 30px; left: 50px; z-index: 1000;
        background: rgba(255,255,255,0.92); padding: 10px 16px;
        border-radius: 8px; border: 1px solid #ccc;
        font-family: Arial; font-size: 12px;
    ">
        <b>🔺 Urgencia</b><br>
        🔴 Alta &nbsp;&nbsp; 🟡 Media &nbsp;&nbsp; 🟢 Baja<br>
        <hr style="margin:4px 0;">
        <b>📍 Marcadores</b><br>
        🔵 Empleado &nbsp; 🎯 Trabajo
    </div>
    """
    mapa.get_root().html.add_child(folium.Element(leyenda_html))

    # ── Añade empleados al mapa ────────────────────────────────
    empleados_con_tareas = {}
    for t in tareas_dia:
        for emp in t.get("employees", []):
            emp_id = emp["id"]
            if emp_id not in empleados_con_tareas:
                empleados_con_tareas[emp_id] = []
            empleados_con_tareas[emp_id].append(t)

    for i, emp in enumerate(empleados):
        if not emp.get("latitude"):
            continue

        color_emp = COLORES_EMPLEADO[i % len(COLORES_EMPLEADO)]
        tareas_emp = empleados_con_tareas.get(emp["id"], [])

        # Popup del empleado
        tareas_html = "".join([
            f"<li>{COLORES_PRIORIDAD[t['priority']]['emoji']} "
            f"<b>{t['title']}</b> · {t.get('start_time','')[:5] if t.get('start_time') else '—'}</li>"
            for t in tareas_emp
        ]) or "<li>Sin tareas hoy</li>"

        popup_emp = f"""
            <div style="font-family:Arial; min-width:200px;">
                <h4 style="margin:0; color:#1a237e;">👷 {emp['name']}</h4>
                <p style="margin:2px 0; color:#666;">{emp.get('role','')}</p>
                <hr style="margin:4px 0;">
                <b>Tareas hoy ({len(tareas_emp)}):</b>
                <ul style="margin:4px 0; padding-left:16px;">
                    {tareas_html}
                </ul>
            </div>
        """

        folium.Marker(
            location=[emp["latitude"], emp["longitude"]],
            popup=folium.Popup(popup_emp, max_width=280),
            tooltip=f"👷 {emp['name']} · {len(tareas_emp)} tarea(s)",
            icon=folium.Icon(color=color_emp, icon="user", prefix="fa")
        ).add_to(mapa)

        # Etiqueta nombre empleado
        folium.Marker(
            location=[emp["latitude"], emp["longitude"]],
            icon=folium.DivIcon(
                html=f"""
                    <div style="
                        font-size:11px; font-weight:bold;
                        color:#1a237e;
                        background:rgba(255,255,255,0.88);
                        padding:2px 6px; border-radius:4px;
                        border:1px solid #3949ab;
                        white-space:nowrap;
                        margin-top:-8px; margin-left:16px;
                    ">{emp['name']}</div>
                """,
                icon_size=(160, 20), icon_anchor=(0, 0)
            )
        ).add_to(mapa)

        # ── Línea de ruta empleado → trabajos ─────────────────
        for t in tareas_emp:
            cliente = t.get("client", {})
            if cliente.get("latitude") and cliente.get("longitude"):
                folium.PolyLine(
                    locations=[
                        [emp["latitude"],       emp["longitude"]],
                        [cliente["latitude"],   cliente["longitude"]]
                    ],
                    color=COLORES_PRIORIDAD[t["priority"]]["hex"],
                    weight=2.5,
                    opacity=0.7,
                    dash_array="6 4",
                    tooltip=f"{emp['name']} → {t['title']}"
                ).add_to(mapa)

    # ── Añade trabajos/tareas al mapa ──────────────────────────
    for t in tareas_dia:
        cliente = t.get("client", {})
        if not cliente.get("latitude"):
            continue

        prioridad = t.get("priority", "media")
        color_t   = COLORES_PRIORIDAD[prioridad]["marker"]
        emoji_t   = COLORES_PRIORIDAD[prioridad]["emoji"]

        empleados_asignados = ", ".join(
            e["name"] for e in t.get("employees", [])
        ) or "Sin asignar"

        hora_i = t.get("start_time", "")[:5] if t.get("start_time") else "—"
        hora_f = t.get("end_time",   "")[:5] if t.get("end_time")   else "—"

        popup_tarea = f"""
            <div style="font-family:Arial; min-width:220px;">
                <h4 style="margin:0; color:{COLORES_PRIORIDAD[prioridad]['hex']};">
                    {emoji_t} {t['title']}
                </h4>
                <hr style="margin:4px 0;">
                <p style="margin:2px 0;">📍 {cliente.get('address','—')}</p>
                <p style="margin:2px 0;">🕐 {hora_i} → {hora_f}</p>
                <p style="margin:2px 0;">👷 {empleados_asignados}</p>
                <p style="margin:2px 0;">📝 {t.get('description') or '—'}</p>
                <hr style="margin:6px 0;">
                <p style="margin:4px 0; font-size:11px; color:#888;">
                    Haz clic en <b>Ver ruta</b> en el panel lateral
                </p>
            </div>
        """

        folium.Marker(
            location=[cliente["latitude"], cliente["longitude"]],
            popup=folium.Popup(popup_tarea, max_width=280),
            tooltip=f"{emoji_t} {t['title']} · {cliente.get('name','—')}",
            icon=folium.Icon(color=color_t, icon="wrench", prefix="fa")
        ).add_to(mapa)

    # ── Layout mapa + panel lateral ────────────────────────────
    col_mapa, col_panel = st.columns([3, 1])

    with col_mapa:
        st.caption(
            "🔵 Empleados · 🎯 Trabajos coloreados por urgencia · "
            "Líneas punteadas = rutas asignadas"
        )
        st_folium(mapa, height=560, use_container_width=True)

    with col_panel:
        st.subheader("📋 Tareas del día")
        st.caption(format_date_es(str(fecha_sel)))

        # Agrupa tareas por prioridad
        for prioridad in ["alta", "media", "baja"]:
            tareas_p = [t for t in tareas_dia if t.get("priority") == prioridad]
            if not tareas_p:
                continue

            emoji = COLORES_PRIORIDAD[prioridad]["emoji"]
            st.markdown(f"**{emoji} Prioridad {prioridad.upper()}**")

            for t in tareas_p:
                cliente   = t.get("client", {})
                empleados_t = [e["name"] for e in t.get("employees", [])]
                hora_i    = t.get("start_time","")[:5] if t.get("start_time") else "—"

                with st.container(border=True):
                    st.markdown(f"**{t['title']}**")
                    st.caption(f"🕐 {hora_i} · 📍 {cliente.get('name','—')}")
                    if empleados_t:
                        st.caption(f"👷 {', '.join(empleados_t)}")

                    # ── Botón Google Maps ──────────────────────
                    dest_lat = cliente.get("latitude")
                    dest_lon = cliente.get("longitude")
                    address  = cliente.get("address", "")

                    if dest_lat and dest_lon:
                        # Usa el primer empleado asignado como origen
                        empleado_origen = next(
                            (e for e in empleados
                             if e["id"] in [x["id"] for x in t.get("employees",[])]
                             and e.get("latitude")),
                            None
                        )

                        if empleado_origen:
                            url = google_maps_url(
                                empleado_origen["latitude"],
                                empleado_origen["longitude"],
                                dest_lat, dest_lon
                            )
                        else:
                            url = google_maps_address_url(address)

                        st.link_button(
                            "🗺️ Ver ruta en Google Maps",
                            url,
                            use_container_width=True
                        )
                    elif address:
                        url = google_maps_address_url(address)
                        st.link_button(
                            "🗺️ Ver en Google Maps",
                            url,
                            use_container_width=True
                        )

except Exception as e:
    st.error(f"❌ Error al cargar el mapa de empleados: {e}")
    st.exception(e)