# Usar una imagen oficial de Python ligera
FROM python:3.11-slim

# Evitar que Python escriba archivos .pyc en el disco y habilitar logs sin buffer
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Establecer el directorio de trabajo en la imagen
WORKDIR /app

# Instalar dependencias del sistema requeridas para instalar ciertas librerías (si hicieran falta)
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copiar el archivo de requerimientos y luego instalar las dependencias
COPY requirements.txt /app/
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copiar todo el contenido del proyecto (desde donde está el Dockerfile) al contenedor
COPY . /app/

# Exponer el puerto por defecto (Railway lo inyectará en la variable $PORT de manera dinámica)
EXPOSE 8000

# Script de inicio embebido que corre migraciones, recolecta estáticos y expone la app.
# En lugar de usar el start_core.sh (que hace 'cd LogisticsCore'), lo hacemos directamente.
CMD python manage.py migrate --noinput && \
    python manage.py collectstatic --noinput && \
    gunicorn LogisticsCore.asgi:application -k uvicorn.workers.UvicornWorker --workers 4 --bind 0.0.0.0:${PORT:-8000}
