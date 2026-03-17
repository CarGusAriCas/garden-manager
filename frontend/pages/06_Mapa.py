"""
Página de mapa de clientes con buscador y filtros.
"""
import streamlit as st
import sys
import os
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import st_folium

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from utils.responsive import apply_responsive_css, mobile_topbar, back_button
from utils.api_client import get_clients, update_client_coordinates, geocode_address

apply_responsive_css()
mobile_topbar()
back_button()

st.set_page_config(page_title="Mapa · GardenManager", page_icon="🗺️", layout="wide")
st.title("🗺️ Mapa de clientes")
st.divider()

def extraer_zona(address: str) -> str:
    """
    Extrae la zona/barrio de una dirección.
    Toma el último fragmento separado por coma como zona.
    """
    if not address:
        return "Sin zona"
    partes = [p.strip() for p in address.split(",")]
    return partes[-1] if len(partes) > 1 else partes[0]


try:
    clientes = get_clients()

    if not clientes:
        st.info("No hay clientes registrados.")
    else:
        # ── Geocodificar clientes sin coordenadas ──────────────
        sin_coords = [c for c in clientes if not c.get("latitude") and c.get("address")]
        if sin_coords:
            col_warn, col_refresh = st.columns([4, 1])
            with col_warn:
                st.warning(f"⚠️ {len(sin_coords)} cliente(s) sin ubicación en el mapa.")
            with col_refresh:
                if st.button("🔄 Refrescar", use_container_width=True):
                    st.cache_data.clear()
                    st.rerun()
            if st.button("🌍 Obtener coordenadas automáticamente", use_container_width=True):
                progress = st.progress(0, text="Iniciando geocodificación...")
                from geopy.geocoders import Nominatim
                from geopy.exc import GeocoderTimedOut, GeocoderUnavailable
                import time

                geolocator = Nominatim(user_agent="garden_manager_mlg_v2", timeout=10)
                ok = 0
                fallo = 0

                for i, c in enumerate(sin_coords):
                    try:
                        location = geolocator.geocode(c["address"])
                        if location:
                            update_client_coordinates(c["id"], location.latitude, location.longitude)
                            c["latitude"]  = location.latitude
                            c["longitude"] = location.longitude
                            ok += 1
                        else:
                            fallo += 1
                    except (GeocoderTimedOut, GeocoderUnavailable):
                        fallo += 1

                    progress.progress(
                        (i + 1) / len(sin_coords),
                        text=f"Geocodificando {i+1}/{len(sin_coords)}: {c['name']}"
                    )
                    time.sleep(1.5)  # Respeta límite Nominatim

                progress.empty()
                st.cache_data.clear()

                if ok > 0:
                    st.success(f"✅ {ok} cliente(s) geocodificados correctamente.")
                if fallo > 0:
                    st.warning(f"⚠️ {fallo} cliente(s) no pudieron geocodificarse.")
                st.rerun()

        # ── Clasificar ─────────────────────────────────────────
        con_coords  = [c for c in clientes if c.get("latitude") and c.get("longitude")]
        sin_dir     = [c for c in clientes if not c.get("address")]
        sin_geocode = [c for c in clientes if c.get("address") and not c.get("latitude")]

        if sin_dir:
            st.warning(f"⚠️ Sin dirección: {', '.join(c['name'] for c in sin_dir)}")
        if sin_geocode:
            st.warning(f"⚠️ Sin geocodificar: {', '.join(c['name'] for c in sin_geocode)}")

        if not con_coords:
            st.info("Ningún cliente tiene coordenadas todavía.")
        else:
            # ── Panel de filtros ───────────────────────────────
            with st.expander("🔍 Buscador y filtros", expanded=True):
                col1, col2, col3 = st.columns(3)

                with col1:
                    busqueda = st.text_input(
                        "🔎 Buscar cliente",
                        placeholder="Nombre, email, teléfono...",
                        help="Busca por nombre, email o teléfono"
                    )

                with col2:
                    # Extrae zonas únicas de las direcciones
                    zonas = sorted(set(
                        extraer_zona(c.get("address", ""))
                        for c in con_coords
                    ))
                    zona_sel = st.multiselect(
                        "📍 Filtrar por zona",
                        options=zonas,
                        default=[],
                        placeholder="Todas las zonas"
                    )

                with col3:
                    orden = st.selectbox(
                        "↕️ Ordenar por",
                        ["Nombre A-Z", "Nombre Z-A", "Zona"]
                    )

            # ── Aplicar filtros ────────────────────────────────
            filtrados = con_coords.copy()

            # Filtro por búsqueda de texto
            if busqueda:
                busqueda_lower = busqueda.lower()
                filtrados = [
                    c for c in filtrados
                    if busqueda_lower in c['name'].lower()
                    or busqueda_lower in (c.get('email') or '').lower()
                    or busqueda_lower in (c.get('phone') or '').lower()
                    or busqueda_lower in (c.get('address') or '').lower()
                ]

            # Filtro por zona
            if zona_sel:
                filtrados = [
                    c for c in filtrados
                    if extraer_zona(c.get("address", "")) in zona_sel
                ]

            # Ordenar
            if orden == "Nombre A-Z":
                filtrados.sort(key=lambda c: c['name'])
            elif orden == "Nombre Z-A":
                filtrados.sort(key=lambda c: c['name'], reverse=True)
            elif orden == "Zona":
                filtrados.sort(key=lambda c: extraer_zona(c.get("address", "")))

            # ── Resumen de resultados ──────────────────────────
            col_res1, col_res2, col_res3 = st.columns(3)
            col_res1.metric("Total clientes", len(con_coords))
            col_res2.metric("Mostrando",      len(filtrados))
            col_res3.metric("Zonas",          len(set(extraer_zona(c.get("address","")) for c in filtrados)))

            if not filtrados:
                st.info("No hay clientes que coincidan con los filtros aplicados.")
            else:
                # ── Mapa ───────────────────────────────────────
                centro_lat = sum(c["latitude"]  for c in filtrados) / len(filtrados)
                centro_lon = sum(c["longitude"] for c in filtrados) / len(filtrados)

                mapa = folium.Map(
                    location=[centro_lat, centro_lon],
                    zoom_start=13,
                    tiles="OpenStreetMap"
                )

                cluster = MarkerCluster(name="Clientes").add_to(mapa)

                # Colores por zona
                colores_zona = {}
                paleta = ["green", "blue", "red", "purple", "orange", "darkgreen", "cadetblue"]
                for i, zona in enumerate(sorted(set(extraer_zona(c.get("address","")) for c in filtrados))):
                    colores_zona[zona] = paleta[i % len(paleta)]

                for c in filtrados:
                    zona  = extraer_zona(c.get("address", ""))
                    color = colores_zona.get(zona, "green")

                    popup_html = f"""
                        <div style="font-family: Arial; min-width: 200px;">
                            <h4 style="margin:0; color:#2D6A4F;">🌿 {c['name']}</h4>
                            <hr style="margin:4px 0;">
                            <p style="margin:2px 0;">📍 {c.get('address', '—')}</p>
                            <p style="margin:2px 0;">📞 {c.get('phone', '—')}</p>
                            <p style="margin:2px 0;">📧 {c.get('email', '—')}</p>
                            <p style="margin:2px 0; color:#2D6A4F;"><b>Zona: {zona}</b></p>
                            <p style="margin:2px 0; color:#888; font-size:11px;">
                                {c.get('notes', '') or ''}
                            </p>
                        </div>
                    """

                    folium.Marker(
                        location=[c["latitude"], c["longitude"]],
                        popup=folium.Popup(popup_html, max_width=280),
                        tooltip=f"🌿 {c['name']} · {zona}",
                        icon=folium.Icon(color=color, icon="leaf", prefix="fa")
                    ).add_to(cluster)

                    # Etiqueta con nombre visible
                    folium.Marker(
                        location=[c["latitude"], c["longitude"]],
                        icon=folium.DivIcon(
                            html=f"""
                                <div style="
                                    font-size: 11px;
                                    font-weight: bold;
                                    color: #1B4332;
                                    background: rgba(255,255,255,0.88);
                                    padding: 2px 6px;
                                    border-radius: 4px;
                                    border: 1px solid #52B788;
                                    white-space: nowrap;
                                    margin-top: -8px;
                                    margin-left: 16px;
                                ">{c['name']}</div>
                            """,
                            icon_size=(160, 20),
                            icon_anchor=(0, 0)
                        )
                    ).add_to(mapa)

                folium.LayerControl().add_to(mapa)

                # ── Layout mapa + lista ────────────────────────
                col_mapa, col_lista = st.columns([3, 1])

                with col_mapa:
                    st.caption(
                        f"🌿 {len(filtrados)} cliente(s) · "
                        f"Los colores indican la zona · "
                        f"Haz clic en un marcador para ver detalles"
                    )
                    mapa_data = st_folium(
                        mapa,
                        height=520,
                        use_container_width=True,
                        returned_objects=["last_object_clicked_popup"]
                    )

                with col_lista:
                    st.subheader("📋 Resultados")
                    clicked = mapa_data.get("last_object_clicked_popup")

                    # Agrupa por zona
                    zonas_presentes = sorted(set(
                        extraer_zona(c.get("address", "")) for c in filtrados
                    ))

                    for zona in zonas_presentes:
                        clientes_zona = [
                            c for c in filtrados
                            if extraer_zona(c.get("address", "")) == zona
                        ]
                        color_zona = colores_zona.get(zona, "green")
                        st.markdown(f"**📍 {zona}** `{len(clientes_zona)}`")

                        for c in clientes_zona:
                            seleccionado = clicked and c['name'] in str(clicked)
                            with st.container(border=True):
                                if seleccionado:
                                    st.markdown(f"**🌿 {c['name']}** ✅")
                                else:
                                    st.markdown(f"**{c['name']}**")
                                if c.get('phone'):
                                    st.caption(f"📞 {c['phone']}")
                                if c.get('email'):
                                    st.caption(f"📧 {c['email']}")

except Exception as e:
    st.error(f"❌ Error al cargar el mapa: {e}")