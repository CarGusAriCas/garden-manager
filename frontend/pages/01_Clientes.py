"""
Página de gestión de clientes.
"""
import streamlit as st
import sys
import os
from utils.responsive import apply_responsive_css, mobile_topbar, back_button
from utils.api_client import get_clients, create_client, update_client, delete_client, format_date_es

apply_responsive_css()
mobile_topbar()
back_button()

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

st.set_page_config(page_title="Clientes · GardenManager", page_icon="👤", layout="wide")
st.title("👤 Gestión de Clientes")
st.divider()

# ── Tabs principales ───────────────────────────────────────────
tab_lista, tab_nuevo = st.tabs(["📋 Lista de clientes", "➕ Nuevo cliente"])

# ── Tab: Lista ─────────────────────────────────────────────────
with tab_lista:
    try:
        clientes = get_clients()
        if not clientes:
            st.info("No hay clientes registrados todavía.")
        else:
            st.caption(f"{len(clientes)} clientes activos")

            for c in clientes:
                with st.expander(f"👤 {c['name']}  —  {c.get('phone', 'Sin teléfono')}"):
                    col1, col2 = st.columns(2)

                    with col1:
                        st.markdown(f"**📧 Email:** {c.get('email') or '—'}")
                        st.markdown(f"**📍 Dirección:** {c.get('address') or '—'}")
                        st.markdown(f"**📝 Notas:** {c.get('notes') or '—'}")
                        st.caption(f"Alta: {format_date_es(c.get('created_at', ''))}")

                    with col2:
                        st.markdown("**✏️ Editar cliente**")
                        with st.form(key=f"edit_{c['id']}"):
                            new_name    = st.text_input("Nombre",    value=c['name'])
                            new_phone   = st.text_input("Teléfono",  value=c.get('phone') or "")
                            new_email   = st.text_input("Email",     value=c.get('email') or "")
                            new_address = st.text_input("Dirección", value=c.get('address') or "")
                            new_notes   = st.text_area("Notas",      value=c.get('notes') or "")

                            col_save, col_del = st.columns(2)
                            with col_save:
                                if st.form_submit_button("💾 Guardar", use_container_width=True):
                                    try:
                                        update_client(c['id'], {
                                            "name":    new_name,
                                            "phone":   new_phone   or None,
                                            "email":   new_email   or None,
                                            "address": new_address or None,
                                            "notes":   new_notes   or None,
                                        })
                                        st.success("Cliente actualizado correctamente.")
                                        st.rerun()
                                    except Exception as e:
                                        st.error(f"Error al actualizar: {e}")
                            with col_del:
                                if st.form_submit_button("🗑️ Desactivar", use_container_width=True):
                                    try:
                                        delete_client(c['id'])
                                        st.warning("Cliente desactivado.")
                                        st.rerun()
                                    except Exception as e:
                                        st.error(f"Error: {e}")

    except Exception as e:
        st.error(f"❌ Error al cargar clientes: {e}")

# ── Tab: Nuevo cliente ─────────────────────────────────────────
with tab_nuevo:
    st.subheader("Registrar nuevo cliente")
    with st.form("form_nuevo_cliente"):
        name    = st.text_input("Nombre completo *", placeholder="María García")
        phone   = st.text_input("Teléfono",          placeholder="612 345 678")
        email   = st.text_input("Email",             placeholder="maria@ejemplo.com")
        address = st.text_input("Dirección",         placeholder="Calle Mayor 12, Madrid")
        notes   = st.text_area("Notas",              placeholder="Observaciones sobre el cliente...")

        submitted = st.form_submit_button("➕ Crear cliente", use_container_width=True)

        if submitted:
            if not name:
                st.error("El nombre es obligatorio.")
            else:
                try:
                    create_client({
                        "name":    name,
                        "phone":   phone   or None,
                        "email":   email   or None,
                        "address": address or None,
                        "notes":   notes   or None,
                    })
                    st.success(f"✅ Cliente '{name}' creado correctamente.")
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Error al crear cliente: {e}")