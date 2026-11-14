# Dockerfile
# Imagen base oficial de Python, version especifica para consistencia.
FROM python:3.13-slim

# Directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia solo los requerimientos primero para aprovechar el cache de Docker
COPY requirements.txt .

# Instala solo las dependencias de ejecucion, verificando sus hashes y
# usando unicamente wheels (sin ejecutar scripts de instalacion).
RUN pip install --no-cache-dir --require-hashes --only-binary :all: -r requirements.txt

# Copia el codigo de la aplicacion (solo la carpeta app)
COPY app/ ./app/

# Ejecuta la aplicacion con un usuario sin privilegios
RUN useradd --create-home appuser
USER appuser

# Gunicorn sirve la aplicacion en el puerto 8000
EXPOSE 8000

# --preload carga la app una sola vez, asi los 4 workers comparten SECRET_KEY
CMD ["gunicorn", "--workers=4", "--preload", "--bind=0.0.0.0:8000", "app.app:app"]
