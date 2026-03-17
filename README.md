# 🌿 GardenManager

API de gestión para empresa de jardinería desarrollada como proyecto de portfolio.

![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=flat&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688?style=flat&logo=fastapi&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.3+-FF4B4B?style=flat&logo=streamlit&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-003B57?style=flat&logo=sqlite&logoColor=white)
![Folium](https://img.shields.io/badge/Folium-Maps-77B829?style=flat&logo=leaflet&logoColor=white)

---

## 📋 Descripción

GardenManager es una aplicación web full-stack para la gestión integral de una empresa de jardinería. Permite gestionar clientes, empleados, planificación de tareas, registro de trabajos realizados, checklists de verificación, incidencias, control de ausencias de personal y visualización geográfica de clientes en mapa interactivo.

Desarrollado con arquitectura modular y separación clara de responsabilidades, preparado para escalar de SQLite a PostgreSQL sin reescribir lógica de negocio.

---

## 🏗️ Arquitectura
```
garden_manager/
│
├── backend/                        # API REST con FastAPI
│   ├── app/
│   │   ├── core/                   # Configuración y conexión BD
│   │   │   ├── config.py           # Settings con Pydantic
│   │   │   └── database.py         # Motor SQLAlchemy + sesiones
│   │   │
│   │   ├── models/                 # Modelos ORM (tablas BD)
│   │   ├── schemas/                # Validación Pydantic (entrada/salida)
│   │   ├── services/               # Lógica de negocio
│   │   ├── routers/                # Endpoints HTTP
│   │   └── main.py                 # Punto de entrada FastAPI
│   │
│   ├── seed.py                     # Script de datos de prueba
│   └── requirements.txt
│
├── frontend/                       # Interfaz con Streamlit
│   ├── pages/                      # Páginas de cada módulo
│   │   ├── 01_Clientes.py
│   │   ├── 02_Empleados.py
│   │   ├── 03_Tareas.py
│   │   ├── 04_Ausencias.py
│   │   ├── 05_Trabajos.py
│   │   └── 06_Mapa.py              # Mapa interactivo con Folium
│   ├── utils/
│   │   └── api_client.py           # Cliente HTTP hacia la API
│   └── Home.py                     # Dashboard principal
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
| **Clientes** | CRUD completo con historial de servicios |
| **Empleados** | Perfiles, especialidades y disponibilidad |
| **Tareas & Agenda** | Planificación semanal con asignación de equipos |
| **Trabajos** | Registro de servicios ejecutados |
| **Checklists** | Listas de verificación e incidencias por trabajo |
| **Ausencias** | Vacaciones, bajas y control de disponibilidad |
| **Dashboard** | Métricas y resumen del estado del negocio |
| **Mapa de clientes** | Mapa interactivo con geocodificación automática, buscador y filtros por zona |

---

## 🛠️ Stack técnico

| Capa | Tecnología | Propósito |
|------|-----------|-----------|
| Backend | **FastAPI** | API REST asíncrona con documentación automática |
| ORM | **SQLAlchemy** | Abstracción de base de datos |
| Validación | **Pydantic v2** | Tipado estricto y validación de datos |
| Base de datos | **SQLite** → **PostgreSQL** | Desarrollo local / producción |
| Frontend | **Streamlit** | Interfaz de usuario rápida |
| HTTP client | **httpx** | Comunicación frontend → backend |
| Mapas | **Folium + streamlit-folium** | Mapas interactivos con Leaflet.js |
| Geocodificación | **Geopy + Nominatim** | Conversión dirección → coordenadas (OpenStreetMap) |

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

Contenido del `.env`:
```
APP_NAME=GardenManager
APP_VERSION=0.1.0
DEBUG=True
DATABASE_URL=sqlite:///./database/garden_manager.db
```

### 5. Inicia el backend
```bash
python -m uvicorn app.main:app --reload
```

El servidor arranca en `http://localhost:8000`.
La documentación interactiva (Swagger UI) está disponible en `http://localhost:8000/docs`.

### 6. Carga datos de prueba (opcional)

Con el servidor activo, en una segunda terminal:
```bash
python seed.py
```

### 7. Inicia el frontend

En una nueva terminal con el venv activo:
```bash
cd ../frontend
streamlit run Home.py
```

La interfaz estará disponible en `http://localhost:8501`.

---

## 📡 API — Endpoints principales

### Clientes `/clients`
| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/clients/` | Lista todos los clientes activos |
| GET | `/clients/{id}` | Obtiene un cliente por ID |
| POST | `/clients/` | Crea un nuevo cliente |
| PUT | `/clients/{id}` | Actualiza un cliente |
| PATCH | `/clients/{id}/coordinates` | Actualiza coordenadas geográficas |
| DELETE | `/clients/{id}` | Desactiva un cliente |

### Empleados `/employees`
| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/employees/` | Lista todos los empleados activos |
| GET | `/employees/available` | Lista empleados disponibles |
| POST | `/employees/` | Crea un nuevo empleado |
| PUT | `/employees/{id}` | Actualiza un empleado |
| DELETE | `/employees/{id}` | Desactiva un empleado |

### Tareas `/tasks`
| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/tasks/` | Lista todas las tareas |
| GET | `/tasks/agenda/day?date=` | Tareas de un día concreto |
| GET | `/tasks/agenda/week?start_date=&end_date=` | Tareas de una semana |
| POST | `/tasks/` | Crea una tarea con empleados asignados |
| PUT | `/tasks/{id}` | Actualiza una tarea |

### Trabajos `/jobs`
| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/jobs/` | Lista todos los trabajos |
| GET | `/jobs/by-task/{task_id}` | Trabajos de una tarea |
| POST | `/jobs/` | Crea un trabajo con checklist |
| PUT | `/jobs/{id}` | Actualiza un trabajo |
| POST | `/jobs/{id}/checklist` | Añade ítem al checklist |
| PATCH | `/jobs/checklist/{item_id}` | Actualiza ítem del checklist |

### Ausencias `/absences`
| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/absences/` | Lista todas las ausencias |
| GET | `/absences/by-employee/{id}` | Ausencias de un empleado |
| GET | `/absences/by-date-range?start=&end=` | Ausencias en un rango |
| GET | `/absences/check-availability/{id}?date=` | Comprueba disponibilidad |
| POST | `/absences/` | Registra una ausencia |
| PUT | `/absences/{id}` | Actualiza o aprueba una ausencia |

---

## 🗺️ Mapa de clientes

El módulo de mapa incluye:

- **Geocodificación automática** — convierte direcciones en coordenadas usando Nominatim (OpenStreetMap), sin coste ni API key
- **Buscador** — filtra por nombre, email, teléfono o dirección
- **Filtros por zona** — agrupa clientes por área geográfica con colores distintivos
- **Marcadores interactivos** — haz clic para ver todos los datos del cliente
- **Agrupación inteligente** — MarkerCluster agrupa marcadores cercanos al alejar el zoom

---

## 🗄️ Escalabilidad — SQLite a PostgreSQL

El proyecto está diseñado para migrar de SQLite a PostgreSQL modificando **una sola línea** en el archivo `.env`:
```bash
# Desarrollo (SQLite)
DATABASE_URL=sqlite:///./database/garden_manager.db

# Producción (PostgreSQL)
DATABASE_URL=postgresql://usuario:contraseña@localhost:5432/garden_manager
```

SQLAlchemy actúa como capa de abstracción — los modelos, servicios y routers no requieren ningún cambio.

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
| 9 | Mapa empleados + rutas Google Maps | 🔜 |

---

## ✅ Buenas prácticas aplicadas

- **Tipado estricto** con Pydantic v2 en todos los schemas
- **Separación de responsabilidades** — models / schemas / services / routers sin dependencias cruzadas
- **Borrado lógico** — los registros nunca se eliminan físicamente, se marcan como inactivos
- **Manejo de errores** centralizado con `HTTPException`
- **Docstrings** en todas las funciones y clases
- **Validaciones de negocio** — detección de solapamiento de ausencias, emails duplicados, IDs inexistentes
- **Datos de prueba** con script `seed.py` reproducible
- **Geocodificación automática** sin dependencias de pago

---

## 👤 Autor

Desarrollado por **CarGusAriCas**
🔗 [github.com/CarGusAriCas](https://github.com/CarGusAriCas)

---

*Proyecto de portfolio — Python + FastAPI + Streamlit*