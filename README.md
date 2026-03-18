# 🌿 GardenManager

API de gestión para empresa de jardinería desarrollada como proyecto de portfolio.

![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=flat&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688?style=flat&logo=fastapi&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.37+-FF4B4B?style=flat&logo=streamlit&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-003B57?style=flat&logo=sqlite&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?style=flat&logo=postgresql&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=flat&logo=docker&logoColor=white)
![Tests](https://img.shields.io/badge/Tests-38%20passing-brightgreen?style=flat)
![JWT](https://img.shields.io/badge/Auth-JWT-000000?style=flat&logo=jsonwebtokens&logoColor=white)
![Twilio](https://img.shields.io/badge/Twilio-WhatsApp-F22F46?style=flat&logo=twilio&logoColor=white)
![Telegram](https://img.shields.io/badge/Telegram-Bot-26A5E4?style=flat&logo=telegram&logoColor=white)

---

## 🌐 Demo en producción

- **Frontend:** https://garden-manager.streamlit.app
- **Backend API:** https://garden-manager-odpo.onrender.com
- **API Docs:** https://garden-manager-odpo.onrender.com/docs

> ⚠️ El backend usa el plan gratuito de Render — puede tardar hasta 50 segundos en despertar tras inactividad.

---

## 📋 Descripción

GardenManager es una aplicación web full-stack para la gestión integral de una empresa de jardinería. Permite gestionar clientes, empleados, planificación de tareas, registro de trabajos realizados, checklists de verificación, incidencias, control de ausencias de personal, visualización geográfica en mapas interactivos, notificaciones automáticas via WhatsApp y Telegram, y sistema de autenticación JWT con roles.

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
│   │   │   ├── security.py         # JWT + bcrypt
│   │   │   ├── email.py            # Cliente SMTP (Mailtrap/Gmail)
│   │   │   ├── twilio_client.py    # Cliente WhatsApp (Twilio)
│   │   │   └── telegram_client.py  # Cliente Telegram Bot
│   │   │
│   │   ├── models/                 # Modelos ORM (tablas BD)
│   │   │   ├── client.py
│   │   │   ├── employee.py
│   │   │   ├── task.py
│   │   │   ├── job.py
│   │   │   ├── absence.py
│   │   │   └── user.py             # Usuarios y roles
│   │   │
│   │   ├── schemas/                # Validación Pydantic (entrada/salida)
│   │   ├── services/               # Lógica de negocio
│   │   ├── routers/                # Endpoints HTTP
│   │   └── main.py                 # Punto de entrada FastAPI
│   │
│   ├── alembic/                    # Migraciones de BD
│   │   └── versions/
│   │
│   ├── tests/                      # Tests con pytest (38/38 ✅)
│   │   ├── conftest.py
│   │   ├── test_clients.py
│   │   ├── test_employees.py
│   │   ├── test_tasks.py
│   │   ├── test_jobs.py
│   │   ├── test_auth.py
│   │   └── test_notifications.py
│   │
│   ├── geocode_clients.py          # Script geocodificación
│   ├── seed.py                     # Script de datos de prueba
│   ├── create_admin.py             # Script creación admin inicial
│   ├── Dockerfile                  # Usuario no-root, healthcheck
│   ├── render.yaml
│   ├── alembic.ini
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
│   │   └── 15_Sugerencias.py       # GitHub Issues integrado
│   ├── utils/
│   │   ├── api_client.py           # Cliente HTTP + caché
│   │   ├── auth.py                 # Gestión de sesión JWT
│   │   ├── responsive.py           # Detección dispositivo + topbar
│   │   └── github_client.py        # API GitHub Issues
│   └── Home.py                     # Dashboard responsive + login
│
├── docker-compose.yml              # PostgreSQL + backend + frontend
├── .env.example
└── README.md
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
| **Clientes** | CRUD completo · historial · coordenadas GPS · código postal |
| **Empleados** | Perfiles · especialidades · WhatsApp · Telegram · GPS |
| **Tareas & Agenda** | Planificación semanal · asignación de equipos · filtros |
| **Trabajos** | Registro de servicios ejecutados · estados |
| **Checklists** | Listas de verificación e incidencias por trabajo |
| **Ausencias** | Vacaciones · bajas · control de disponibilidad |
| **Dashboard** | Métricas responsive · gráficos Plotly · selector de semana |
| **Mapa clientes** | Geocodificación automática · buscador · filtros por zona |
| **Mapa empleados** | Rutas · urgencia por color · GPS real · Google Maps |
| **Notificaciones** | WhatsApp (Twilio) · Telegram Bot · plantillas automáticas |
| **Autenticación** | JWT · roles (admin/encargado/empleado) · activación por email |
| **Sugerencias** | Integración directa con GitHub Issues · notificación Telegram |

---

## 🔐 Sistema de autenticación

### Roles y permisos

| Rol | Acceso |
|-----|--------|
| **admin** | Todo + gestión de usuarios |
| **encargado** | Todo excepto gestión de usuarios |
| **empleado** | Solo sus tareas, agenda, ausencias y rutas |

### Flujo de activación
```
Admin crea usuario
      ↓
Sistema genera contraseña segura automática
      ↓
Email de activación enviado (Mailtrap dev / Gmail prod)
      ↓
Usuario activa cuenta y cambia contraseña
      ↓
Login con JWT (válido 8 horas)
```

---

## 🛠️ Stack técnico

| Capa | Tecnología | Propósito |
|------|-----------|-----------|
| Backend | **FastAPI** | API REST con documentación automática |
| ORM | **SQLAlchemy** | Abstracción de base de datos |
| Validación | **Pydantic v2** | Tipado estricto y validación |
| Autenticación | **JWT + bcrypt** | Tokens seguros y hashing de contraseñas |
| Base de datos | **SQLite** → **PostgreSQL** | Desarrollo / producción |
| Migraciones | **Alembic** | Control de versiones de BD |
| Frontend | **Streamlit** | Interfaz responsive |
| Gráficos | **Plotly** | Dashboards interactivos |
| HTTP client | **httpx** | Comunicación frontend → backend |
| Mapas | **Folium + streamlit-folium** | Mapas interactivos Leaflet.js |
| Geocodificación | **Geopy + Nominatim** | Dirección → coordenadas |
| WhatsApp | **Twilio** | Mensajería WhatsApp Business |
| Telegram | **python-telegram-bot** | Bot de notificaciones |
| Email | **SMTP** | Activación de cuentas (Mailtrap/Gmail) |
| Contenedores | **Docker + Docker Compose** | Despliegue reproducible |
| Tests | **pytest + httpx** | 38 tests automatizados |
| Issues | **GitHub API** | Seguimiento de sugerencias |

---

## 🚀 Instalación y puesta en marcha

### Requisitos previos

- Python 3.11 o superior
- Git
- Docker Desktop (opcional)

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
```bash
cp .env.example .env
```

Edita `.env` con tus valores:
```env
APP_NAME=GardenManager
DATABASE_URL=sqlite:///./database/garden_manager.db
SECRET_KEY=genera_con_secrets.token_hex(32)
API_URL=http://localhost:8000
FRONTEND_URL=http://localhost:8501

# Email (Mailtrap dev / Gmail prod)
MAIL_SERVER=sandbox.smtp.mailtrap.io
MAIL_PORT=587
MAIL_USERNAME=tu_usuario_mailtrap
MAIL_PASSWORD=tu_password_mailtrap

# GitHub
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

### 5. Aplica las migraciones
```bash
alembic upgrade head
```

### 6. Crea el usuario admin
```bash
python create_admin.py
```

### 7. Ejecuta los tests
```bash
pytest tests/ -v
# 38 passed ✅
```

### 8. Inicia el backend
```bash
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Documentación interactiva en `http://localhost:8000/docs`

### 9. Carga datos de prueba
```bash
python seed.py
python geocode_clients.py
```

### 10. Inicia el frontend
```bash
cd ../frontend
streamlit run Home.py
```

Interfaz disponible en `http://localhost:8501`

---

## 🐳 Docker
```bash
# Construir y arrancar todos los servicios
docker compose up --build

# Solo arrancar (si ya está construido)
docker compose up -d

# Ver logs
docker compose logs backend
```

Servicios disponibles:
- **Frontend:** http://localhost:8501
- **Backend:** http://localhost:8000
- **PostgreSQL:** localhost:5432

---

## 📡 API — Endpoints principales

### Autenticación `/auth`
| Método | Endpoint | Descripción |
|--------|----------|-------------|
| POST | `/auth/login` | Login con email y contraseña |
| POST | `/auth/users` | Crea usuario (admin) |
| POST | `/auth/activate` | Activa cuenta con token |
| POST | `/auth/reset-password/request` | Solicita reset de contraseña |
| POST | `/auth/reset-password/confirm` | Confirma reset con token |
| GET | `/auth/me` | Datos del usuario autenticado |

### Clientes `/clients`
| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/clients/` | Lista clientes activos |
| POST | `/clients/` | Crea cliente |
| PUT | `/clients/{id}` | Actualiza cliente |
| PATCH | `/clients/{id}/coordinates` | Actualiza coordenadas GPS |
| POST | `/clients/geocode-all` | Geocodifica todos los clientes |

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

### Notificaciones `/notifications`
| Método | Endpoint | Descripción |
|--------|----------|-------------|
| POST | `/notifications/test-telegram` | Test conexión Telegram |
| POST | `/notifications/test-whatsapp` | Test conexión WhatsApp |
| POST | `/notifications/tarea-asignada` | Notifica tarea a empleado |
| POST | `/notifications/recordatorio` | Recordatorio de tareas |
| POST | `/notifications/ausencia` | Resultado solicitud ausencia |
| POST | `/notifications/trabajo-completado` | Aviso al cliente |
| POST | `/notifications/nueva-sugerencia` | Notifica sugerencia al admin |

---

## ✅ Tests
```bash
pytest tests/ -v
# 38 passed in ~10s
```

| Módulo | Tests |
|--------|-------|
| Clientes | 9 tests — CRUD completo + borrado lógico |
| Empleados | 7 tests — CRUD + disponibilidad |
| Tareas | 6 tests — CRUD + agenda día/semana |
| Ausencias | 3 tests — creación + validación + disponibilidad |
| Trabajos | 8 tests — CRUD + checklist + incidencias |
| Autenticación | 9 tests — login + activación + JWT |
| Notificaciones | 5 tests — endpoints + validación |

---

## 🗄️ Escalabilidad — SQLite a PostgreSQL
```env
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
| 10 | Tests pytest 38/38 | ✅ |
| 11 | Notificaciones WhatsApp + Telegram | ✅ |
| 12 | Docker + PostgreSQL | ✅ |
| 13 | Alembic migraciones | ✅ |
| 14 | Despliegue Render + Streamlit Cloud | ✅ |
| 15 | Login JWT + roles | ✅ |
| 16 | Dashboard con gráficos Plotly | ✅ |
| 17 | App de clientes | 🔜 |

---

## ✅ Buenas prácticas aplicadas

- **Tipado estricto** con Pydantic v2 en todos los schemas
- **Separación de responsabilidades** — models / schemas / services / routers
- **Borrado lógico** — los registros nunca se eliminan físicamente
- **Manejo de errores** centralizado con `HTTPException`
- **Docstrings** en todas las funciones y clases
- **Tests automatizados** — 38 tests, 0 warnings
- **Caché en frontend** — `@st.cache_data` con TTL configurable
- **Eager loading** con `joinedload` — elimina el problema N+1
- **JWT + bcrypt** — autenticación segura estándar de la industria
- **Dockerfiles seguros** — usuario no-root, healthcheck, sin caché pip
- **Migraciones con Alembic** — control de versiones de BD sin pérdida de datos
- **Variables de entorno** — secretos nunca en el código

---

## 👤 Autor

Desarrollado por **CarGusAriCas**
🔗 [github.com/CarGusAriCas](https://github.com/CarGusAriCas)
💼 [linkedin.com/in/carlos-arias-castillo](https://www.linkedin.com/in/carlos-arias-castillo/)

---

*Proyecto de portfolio — Python + FastAPI + Streamlit · 2025-2026*