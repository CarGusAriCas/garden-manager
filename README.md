# 🌿 GardenManager

API de gestión para empresa de jardinería desarrollada como proyecto de portfolio.

![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=flat&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688?style=flat&logo=fastapi&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.3+-FF4B4B?style=flat&logo=streamlit&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-003B57?style=flat&logo=sqlite&logoColor=white)
![Folium](https://img.shields.io/badge/Folium-Maps-77B829?style=flat)
![Tests](https://img.shields.io/badge/Tests-24%20passing-brightgreen?style=flat)
![Twilio](https://img.shields.io/badge/Twilio-WhatsApp-F22F46?style=flat&logo=twilio&logoColor=white)
![Telegram](https://img.shields.io/badge/Telegram-Bot-26A5E4?style=flat&logo=telegram&logoColor=white)

---

## 📋 Descripción

GardenManager es una aplicación web full-stack para la gestión integral de una empresa de jardinería. Permite gestionar clientes, empleados, planificación de tareas, registro de trabajos realizados, checklists de verificación, incidencias, control de ausencias de personal, visualización geográfica en mapas interactivos y notificaciones automáticas via WhatsApp y Telegram.

Desarrollado con arquitectura modular y separación clara de responsabilidades, preparado para escalar de SQLite a PostgreSQL sin reescribir lógica de negocio.

---

## 🏗️ Arquitectura
```
garden_manager/
│
├── backend/                        # API REST con FastAPI
│   ├── app/
│   │   ├── core/                   # Configuración y conexión BD
│   │   │   ├── config.py           # Settings con Pydantic v2
│   │   │   ├── database.py         # Motor SQLAlchemy + sesiones
│   │   │   ├── twilio_client.py    # Cliente WhatsApp (Twilio)
│   │   │   └── telegram_client.py  # Cliente Telegram Bot
│   │   │
│   │   ├── models/                 # Modelos ORM (tablas BD)
│   │   ├── schemas/                # Validación Pydantic (entrada/salida)
│   │   ├── services/               # Lógica de negocio
│   │   ├── routers/                # Endpoints HTTP
│   │   └── main.py                 # Punto de entrada FastAPI
│   │
│   ├── tests/                      # Tests con pytest (24/24 ✅)
│   │   ├── conftest.py
│   │   ├── test_clients.py
│   │   ├── test_employees.py
│   │   └── test_tasks.py
│   │
│   ├── geocode_clients.py          # Script geocodificación
│   ├── seed.py                     # Script de datos de prueba
│   └── requirements.txt
│
├── frontend/                       # Interfaz con Streamlit
│   ├── pages/
│   │   ├── 01_Clientes.py
│   │   ├── 02_Empleados.py
│   │   ├── 03_Tareas.py
│   │   ├── 04_Ausencias.py
│   │   ├── 05_Trabajos.py
│   │   ├── 06_Mapa.py              # Mapa interactivo clientes
│   │   ├── 07_Mapa_Empleados.py    # Mapa rutas + GPS empleados
│   │   ├── 10_Notificaciones.py    # Panel WhatsApp + Telegram
│   │   └── 15_Sugerencias.py      # GitHub Issues integrado
│   ├── utils/
│   │   ├── api_client.py           # Cliente HTTP + caché
│   │   ├── responsive.py           # Detección dispositivo + topbar
│   │   └── github_client.py        # API GitHub Issues
│   └── Home.py                     # Dashboard responsive
│
└── database/                       # Archivo SQLite (local)
```

### Flujo de una petición
```
Streamlit → api_client.py → routers/ → services/ → models/ → BD
                                ↑             ↓
                            schemas/      schemas/
                          (validación)  (respuesta)
```

---

## 🧩 Módulos

| Módulo | Descripción |
|--------|-------------|
| **Clientes** | CRUD completo · historial · coordenadas GPS |
| **Empleados** | Perfiles · especialidades · WhatsApp · Telegram |
| **Tareas & Agenda** | Planificación semanal · asignación de equipos |
| **Trabajos** | Registro de servicios ejecutados |
| **Checklists** | Listas de verificación e incidencias por trabajo |
| **Ausencias** | Vacaciones · bajas · control de disponibilidad |
| **Dashboard** | Métricas responsive · móvil · tablet · desktop |
| **Mapa clientes** | Geocodificación automática · buscador · filtros por zona |
| **Mapa empleados** | Rutas · urgencia por color · GPS real · Google Maps |
| **Notificaciones** | WhatsApp (Twilio) · Telegram Bot · plantillas automáticas |
| **Sugerencias** | Integración directa con GitHub Issues |

---

## 🛠️ Stack técnico

| Capa | Tecnología | Propósito |
|------|-----------|-----------|
| Backend | **FastAPI** | API REST con documentación automática |
| ORM | **SQLAlchemy** | Abstracción de base de datos |
| Validación | **Pydantic v2** | Tipado estricto y validación |
| Base de datos | **SQLite** → **PostgreSQL** | Desarrollo / producción |
| Frontend | **Streamlit** | Interfaz responsive |
| HTTP client | **httpx** | Comunicación frontend → backend |
| Mapas | **Folium + streamlit-folium** | Mapas interactivos Leaflet.js |
| Geocodificación | **Geopy + Nominatim** | Dirección → coordenadas |
| WhatsApp | **Twilio** | Mensajería WhatsApp Business |
| Telegram | **python-telegram-bot** | Bot de notificaciones |
| Tests | **pytest + httpx** | 24 tests automatizados |
| Issues | **GitHub API** | Seguimiento de sugerencias |

---

## 🚀 Instalación y puesta en marcha

### Requisitos previos

- Python 3.11 o superior
- Git

### 1. Clona el repositorio
```bash
git clone https://github.com/CarGusAriCas/garden-manager.git
cd garden-manager
```

### 2. Crea y activa el entorno virtual
```bash
cd backend
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### 3. Instala las dependencias
```bash
pip install -r requirements.txt
```

### 4. Configura las variables de entorno

Crea el archivo `.env` dentro de `backend/` copiando el ejemplo:
```bash
cp .env.example .env
```

Edita `.env` con tus valores:
```env
APP_NAME=GardenManager
APP_VERSION=0.1.0
DEBUG=True
DATABASE_URL=sqlite:///./database/garden_manager.db
API_URL=http://localhost:8000

# GitHub (para sugerencias)
GITHUB_TOKEN=tu_token
GITHUB_REPO=usuario/garden-manager

# Twilio WhatsApp
TWILIO_ACCOUNT_SID=ACxxxxxxxx
TWILIO_AUTH_TOKEN=xxxxxxxx
TWILIO_WHATSAPP_FROM=whatsapp:+14155238886

# Telegram
TELEGRAM_TOKEN=xxxxxxxx:AAHxxxxxxxx
TELEGRAM_CHAT_ID=123456789
```

### 5. Ejecuta los tests
```bash
pytest tests/ -v
```

Resultado esperado: **24 passed, 0 warnings**

### 6. Inicia el backend
```bash
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Documentación interactiva en `http://localhost:8000/docs`

### 7. Carga datos de prueba
```bash
python seed.py
python geocode_clients.py  # Geocodifica las direcciones
```

### 8. Inicia el frontend
```bash
cd ../frontend
streamlit run Home.py
```

Interfaz disponible en `http://localhost:8501`

---

## 📡 API — Endpoints principales

### Clientes `/clients`
| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/clients/` | Lista clientes activos |
| POST | `/clients/` | Crea cliente |
| PUT | `/clients/{id}` | Actualiza cliente |
| PATCH | `/clients/{id}/coordinates` | Actualiza coordenadas GPS |
| DELETE | `/clients/{id}` | Desactiva cliente |

### Empleados `/employees`
| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/employees/` | Lista empleados activos |
| GET | `/employees/available` | Empleados disponibles |
| POST | `/employees/` | Crea empleado |
| PATCH | `/employees/{id}/coordinates` | Actualiza coordenadas GPS |

### Tareas `/tasks`
| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/tasks/agenda/day?date=` | Tareas de un día |
| GET | `/tasks/agenda/week?start_date=&end_date=` | Tareas de una semana |
| POST | `/tasks/` | Crea tarea con empleados |
| PUT | `/tasks/{id}` | Actualiza tarea |

### Trabajos `/jobs`
| Método | Endpoint | Descripción |
|--------|----------|-------------|
| POST | `/jobs/` | Crea trabajo con checklist |
| POST | `/jobs/{id}/checklist` | Añade ítem al checklist |
| PATCH | `/jobs/checklist/{item_id}` | Actualiza ítem / incidencia |

### Ausencias `/absences`
| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/absences/check-availability/{id}?date=` | Comprueba disponibilidad |
| POST | `/absences/` | Registra ausencia |
| PUT | `/absences/{id}` | Aprueba / deniega ausencia |

### Notificaciones `/notifications`
| Método | Endpoint | Descripción |
|--------|----------|-------------|
| POST | `/notifications/test-telegram` | Test conexión Telegram |
| POST | `/notifications/test-whatsapp` | Test conexión WhatsApp |
| POST | `/notifications/tarea-asignada` | Notifica tarea a empleado |
| POST | `/notifications/recordatorio` | Recordatorio de tareas |
| POST | `/notifications/ausencia` | Resultado solicitud ausencia |
| POST | `/notifications/trabajo-completado` | Aviso al cliente |
| POST | `/notifications/mensaje-libre` | Mensaje personalizado |

---

## 🗺️ Mapas

- **Geocodificación automática** via Nominatim (OpenStreetMap), sin coste
- **Buscador y filtros** por nombre, zona y prioridad
- **GPS real** del empleado via API del navegador
- **Rutas Google Maps** con un clic desde el panel lateral
- **Colores por urgencia** — rojo alta, naranja media, verde baja

---

## 📱 Responsive

La interfaz se adapta automáticamente al dispositivo:

| Dispositivo | Vista |
|-------------|-------|
| **Móvil** | Topbar con iconos grandes · accesos directos · alertas prioritarias |
| **Tablet** | Grid 2 columnas · métricas compactas |
| **Desktop** | Dashboard completo 3 columnas · todas las métricas |

---

## ✅ Tests
```bash
pytest tests/ -v
# 24 passed in ~5s
```

| Módulo | Tests |
|--------|-------|
| Clientes | 9 tests — CRUD completo + borrado lógico |
| Empleados | 7 tests — CRUD + disponibilidad |
| Tareas | 5 tests — CRUD + agenda día/semana |
| Ausencias | 3 tests — creación + validación + disponibilidad |

---

## 🗄️ Escalabilidad — SQLite a PostgreSQL
```bash
# Desarrollo
DATABASE_URL=sqlite:///./database/garden_manager.db

# Producción
DATABASE_URL=postgresql://usuario:contraseña@localhost:5432/garden_manager
```

SQLAlchemy actúa como capa de abstracción — ningún modelo, servicio ni router requiere cambios.

---

## 🗺️ Roadmap

| Fase | Módulo | Estado |
|------|--------|--------|
| 1 | Core + Setup | ✅ |
| 2 | Clientes | ✅ |
| 3 | Empleados | ✅ |
| 4 | Tareas & Agenda | ✅ |
| 5 | Trabajos & Checklists | ✅ |
| 6 | Ausencias | ✅ |
| 7 | Frontend Streamlit | ✅ |
| 8 | README & Documentación | ✅ |
| 9 | Mapa empleados + rutas Google Maps | ✅ |
| 10 | Tests pytest 24/24 | ✅ |
| 11 | Notificaciones WhatsApp + Telegram | ✅ |
| 12 | Despliegue en producción | 🔜 |

---

## ✅ Buenas prácticas aplicadas

- **Tipado estricto** con Pydantic v2 en todos los schemas
- **Separación de responsabilidades** — models / schemas / services / routers
- **Borrado lógico** — los registros nunca se eliminan físicamente
- **Manejo de errores** centralizado con `HTTPException`
- **Docstrings** en todas las funciones y clases
- **Tests automatizados** — 24 tests, 0 warnings
- **Caché en frontend** — `@st.cache_data` con TTL configurable
- **Eager loading** con `joinedload` — elimina el problema N+1
- **Índices en BD** en columnas de búsqueda frecuente

---

## 👤 Autor

Desarrollado por **CarGusAriCas**
🔗 [github.com/CarGusAriCas](https://github.com/CarGusAriCas)

---

*Proyecto de portfolio — Python + FastAPI + Streamlit*