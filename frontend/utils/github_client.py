"""
Cliente para la API de GitHub.
Permite crear issues directamente desde la aplicación.
"""
import httpx
import os
from datetime import datetime


def _get_token() -> str:
    """Lee el token de GitHub en tiempo de ejecución."""
    return os.getenv("GITHUB_TOKEN", "")


def _get_repo() -> str:
    """Lee el repositorio de GitHub en tiempo de ejecución."""
    return os.getenv("GITHUB_REPO", "CarGusAriCas/garden-manager")


GITHUB_API = "https://api.github.com"

ETIQUETAS_DISPONIBLES = {
    "💡 Nueva funcionalidad": "enhancement",
    "🐛 Error o problema":    "bug",
    "🎨 Mejora visual":       "ui",
    "⚡ Rendimiento":         "performance",
    "📱 Adaptación móvil":    "mobile",
    "🗺️ Mapas y rutas":      "maps",
    "📊 Informes":            "reports",
    "🔐 Seguridad":           "security",
    "📝 Documentación":       "documentation",
    "❓ Pregunta o duda":      "question",
}

PRIORIDADES = {
    "🔴 Alta":  "priority: high",
    "🟡 Media": "priority: medium",
    "🟢 Baja":  "priority: low",
}

MODULOS = [
    "General",
    "Clientes",
    "Empleados",
    "Tareas & Agenda",
    "Trabajos & Checklists",
    "Ausencias",
    "Dashboard",
    "Mapa de clientes",
    "Mapa de empleados",
    "Rendimiento",
    "Móvil / Responsive",
]


def crear_issue(
    titulo:      str,
    descripcion: str,
    etiqueta:    str,
    prioridad:   str,
    modulo:      str,
    autor:       str = "Usuario de la app",
) -> dict:
    """
    Crea un issue en el repositorio de GitHub.

    Args:
        titulo:      Título del issue
        descripcion: Descripción detallada
        etiqueta:    Etiqueta del tipo de issue
        prioridad:   Nivel de prioridad
        modulo:      Módulo al que afecta
        autor:       Nombre del usuario que reporta

    Returns:
        Diccionario con url y número del issue creado

    Raises:
        Exception: Si la API de GitHub devuelve un error
    """
    token = _get_token()
    if not token:
        raise Exception("Token de GitHub no configurado en .env")

    body = f"""
## 📋 Descripción
{descripcion}

---

## 🔍 Detalles
| Campo | Valor |
|-------|-------|
| **Módulo** | {modulo} |
| **Tipo** | {etiqueta} |
| **Prioridad** | {prioridad} |
| **Reportado por** | {autor} |
| **Fecha** | {datetime.now().strftime("%d/%m/%Y %H:%M")} |

---
*Issue creado automáticamente desde GardenManager App*
    """.strip()

    labels = [
        ETIQUETAS_DISPONIBLES.get(etiqueta, "enhancement"),
        PRIORIDADES.get(prioridad, "priority: medium"),
        f"módulo: {modulo.lower()}",
    ]

    payload = {
        "title":  f"[{modulo}] {titulo}",
        "body":   body,
        "labels": labels,
    }

    headers = {
        "Authorization":        f"Bearer {token}",
        "Accept":               "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }

    response = httpx.post(
        f"{GITHUB_API}/repos/{_get_repo()}/issues",
        json=payload,
        headers=headers,
        timeout=10
    )

    if response.status_code == 201:
        data = response.json()
        return {
            "numero": data["number"],
            "url":    data["html_url"],
            "titulo": data["title"],
        }
    else:
        raise Exception(f"Error GitHub API {response.status_code}: {response.text}")


def listar_issues(estado: str = "open") -> list:
    """
    Lista los issues del repositorio.

    Args:
        estado: 'open', 'closed' o 'all'

    Returns:
        Lista de issues
    """
    token = _get_token()
    if not token:
        return []

    headers = {
        "Authorization": f"Bearer {token}",
        "Accept":        "application/vnd.github+json",
    }

    response = httpx.get(
        f"{GITHUB_API}/repos/{_get_repo()}/issues",
        params={"state": estado, "per_page": 20},
        headers=headers,
        timeout=10
    )

    if response.status_code == 200:
        return response.json()
    return []