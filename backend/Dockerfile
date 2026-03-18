# Imagen base Python oficial (slim = menor superficie de ataque)
FROM python:3.11-slim

# Metadatos de la imagen
LABEL maintainer="CarGusAriCas"
LABEL description="GardenManager API - FastAPI Backend"

# Crea usuario sin privilegios — nunca ejecutar como root en producción
RUN groupadd -r garden && useradd -r -g garden garden

# Directorio de trabajo dentro del contenedor
WORKDIR /app

# Instala dependencias del sistema mínimas
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        gcc \
        libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copia primero requirements para aprovechar caché de Docker
# Si requirements.txt no cambia, esta capa se reutiliza
COPY requirements.txt .

# Instala dependencias Python sin caché para reducir tamaño
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copia el resto del código
COPY . .

# Cambia la propiedad de los archivos al usuario sin privilegios
RUN chown -R garden:garden /app

# Cambia al usuario sin privilegios
USER garden

# Puerto que expone el contenedor
EXPOSE 8000

# Healthcheck — Docker verifica que la app responde
HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
    CMD python -c "import httpx; httpx.get('http://localhost:8000/health')" || exit 1

# Ejecuta migraciones y arranca el servidor
CMD ["sh", "-c", "alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port $PORT"]