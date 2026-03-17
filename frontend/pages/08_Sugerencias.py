"""
Página de sugerencias y seguimiento de mejoras.
Permite crear issues en GitHub directamente desde la app.
"""
import streamlit as st
import sys
import os
from dotenv import load_dotenv

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from utils.responsive import apply_responsive_css, mobile_topbar, back_button
from utils.github_client import (
    crear_issue, listar_issues,
    ETIQUETAS_DISPONIBLES, PRIORIDADES, MODULOS
)

load_dotenv(os.path.join(os.path.dirname(__file__), "../../backend/.env"))
apply_responsive_css()
mobile_topbar()
back_button()

st.set_page_config(
    page_title="Sugerencias · GardenManager",
    page_icon="💡",
    layout="wide"
)
st.title("💡 Sugerencias y mejoras")
st.caption("Envía tus ideas directamente al equipo de desarrollo")
st.divider()

tab_nueva, tab_ver = st.tabs(["➕ Nueva sugerencia", "📋 Sugerencias enviadas"])

# ── Tab: Nueva sugerencia ──────────────────────────────────────
with tab_nueva:
    st.subheader("Reportar una mejora o incidencia")

    with st.form("form_sugerencia"):
        autor = st.text_input(
            "Tu nombre",
            placeholder="¿Quién reporta esto?",
            help="Opcional — para saber quién envió la sugerencia"
        )

        titulo = st.text_input(
            "Título *",
            placeholder="Resumen breve de la sugerencia o problema",
            max_chars=100
        )

        col1, col2, col3 = st.columns(3)
        with col1:
            etiqueta = st.selectbox(
                "Tipo *",
                list(ETIQUETAS_DISPONIBLES.keys())
            )
        with col2:
            prioridad = st.selectbox(
                "Prioridad *",
                list(PRIORIDADES.keys())
            )
        with col3:
            modulo = st.selectbox(
                "Módulo *",
                MODULOS
            )

        descripcion = st.text_area(
            "Descripción detallada *",
            placeholder=(
                "Describe con detalle:\n"
                "- ¿Qué necesitas o qué falla?\n"
                "- ¿En qué situación ocurre?\n"
                "- ¿Cómo debería funcionar idealmente?"
            ),
            height=180
        )

        submitted = st.form_submit_button(
            "📤 Enviar sugerencia",
            use_container_width=True
        )

        if submitted:
            if not titulo:
                st.error("El título es obligatorio.")
            elif not descripcion:
                st.error("La descripción es obligatoria.")
            else:
                with st.spinner("Enviando sugerencia a GitHub..."):
                    try:
                        resultado = crear_issue(
                            titulo=titulo,
                            descripcion=descripcion,
                            etiqueta=etiqueta,
                            prioridad=prioridad,
                            modulo=modulo,
                            autor=autor or "Usuario anónimo",
                        )
                        st.success(
                            f"✅ Sugerencia enviada correctamente · "
                            f"Issue #{resultado['numero']}"
                        )
                        st.link_button(
                            f"🔗 Ver en GitHub · #{resultado['numero']}",
                            resultado["url"],
                            use_container_width=True
                        )
                    except Exception as e:
                        st.error(f"❌ Error al enviar: {e}")

# ── Tab: Ver sugerencias ───────────────────────────────────────
with tab_ver:
    st.subheader("Sugerencias enviadas")

    col_f1, col_f2 = st.columns(2)
    with col_f1:
        filtro_estado = st.selectbox(
            "Estado",
            ["Abiertas", "Cerradas", "Todas"]
        )
    with col_f2:
        if st.button("🔄 Actualizar", use_container_width=True):
            st.rerun()

    estado_map = {
        "Abiertas": "open",
        "Cerradas": "closed",
        "Todas":    "all"
    }

    with st.spinner("Cargando sugerencias de GitHub..."):
        try:
            issues = listar_issues(estado_map[filtro_estado])

            if not issues:
                st.info("No hay sugerencias en este estado.")
            else:
                st.caption(f"{len(issues)} sugerencia(s)")

                for issue in issues:
                    estado_icon = "🟢" if issue["state"] == "open" else "✅"
                    etiquetas   = [label["name"] for label in issue.get("labels", [])]
                    fecha       = issue["created_at"][:10]

                    with st.expander(
                        f"{estado_icon} #{issue['number']} · {issue['title']}"
                    ):
                        col1, col2 = st.columns([3, 1])

                        with col1:
                            if issue.get("body"):
                                # Muestra solo el bloque de descripción
                                body = issue["body"]
                                if "## 📋 Descripción" in body:
                                    desc = body.split("---")[0].replace(
                                        "## 📋 Descripción", ""
                                    ).strip()
                                    st.markdown(desc)
                                else:
                                    st.markdown(body[:300])

                        with col2:
                            st.markdown(f"**📅 Fecha:** {fecha}")
                            if etiquetas:
                                st.markdown("**🏷️ Etiquetas:**")
                                for etiq in etiquetas:
                                    st.caption(f"• {etiq}")
                            st.link_button(
                                "🔗 Ver en GitHub",
                                issue["html_url"],
                                use_container_width=True
                            )

        except Exception as e:
            st.error(f"❌ Error al cargar issues: {e}")