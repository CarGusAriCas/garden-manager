# Imagen base Python oficial (slim = menor superficie de ataque)
FROM python:3.11-slim

# Metadatos de la imagen
LABEL maintainer="CarGusAriCas"
LABEL description="GardenManager - Streamlit Frontend"

# Crea usuario sin privilegios
RUN groupadd -r garden && useradd -r -g garden garden

# Directorio de trabajo
WORKDIR /app

# Instala dependencias del sistema mínimas
RUN apt-get update \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copia requirements primero para aprovechar caché
COPY requirements-frontend.txt .

# Instala dependencias Python sin caché
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements-frontend.txt

# Copia el código del frontend
COPY . .

# Cambia la propiedad al usuario sin privilegios
RUN chown -R garden:garden /app

# Cambia al usuario sin privilegios
USER garden

# Puerto de Streamlit
EXPOSE 8501

# Configuración de Streamlit para producción
ENV STREAMLIT_SERVER_HEADLESS=true
ENV STREAMLIT_SERVER_PORT=8501
ENV STREAMLIT_SERVER_ADDRESS=0.0.0.0
ENV STREAMLIT_BROWSER_GATHER_USAGE_STATS=false

# Healthcheck
HEALTHCHECK --interval=30s --timeout=10s --start-period=15s --retries=3 \
    CMD python -c "import httpx; httpx.get('http://localhost:8501/_stcore/health')" || exit 1

# Comando de arranque
CMD ["streamlit", "run", "Home.py"]