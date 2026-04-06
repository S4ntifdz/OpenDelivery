#!/bin/bash
# Navegar al directorio donde está manage.py si ejecutamos desde afuera
if [ -d "LogisticsCore" ] && [ -f "LogisticsCore/manage.py" ]; then
    cd LogisticsCore
fi

echo "Corriendo migraciones de base de datos..."
python manage.py migrate --noinput

echo "Recolectando archivos estáticos para el Admin..."
python manage.py collectstatic --noinput

echo "Iniciando la aplicación web..."
# Recomendación real para Railway: usar Uvicorn o Gunicorn en producción
# Si instalás uvicorn, reemplazá la línea de abajo por:
# exec uvicorn LogisticsCore.asgi:application --host 0.0.0.0 --port ${PORT:-8000}

gunicorn LogisticsCore.asgi:application -k uvicorn.workers.UvicornWorker --workers 4 --bind 0.0.0.0:${PORT:-8000}
