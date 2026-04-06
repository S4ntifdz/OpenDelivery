#!/bin/bash
# Navegar al directorio donde está manage.py si ejecutamos desde afuera
if [ -d "LogisticsCore" ] && [ -f "LogisticsCore/manage.py" ]; then
    cd LogisticsCore
fi

echo "Iniciando Celery Beat..."
# Celery Beat se encarga de disparar las tareas programadas (cron jobs)
# Borramos el archivo PID por si quedó 'trabado' de un reinicio forzado
rm -f celerybeat.pid

exec celery -A LogisticsCore beat --loglevel=info
