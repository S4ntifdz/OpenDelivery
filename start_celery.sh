#!/bin/bash
# Navegar al directorio donde está manage.py si ejecutamos desde afuera
if [ -d "LogisticsCore" ] && [ -f "LogisticsCore/manage.py" ]; then
    cd LogisticsCore
fi

echo "Iniciando Celery Worker..."
# El worker procesa los envíos encolados asincrónicamente
# Limitamos la concurrencia para evitar que Railway mate el contenedor por falta de memoria RAM
exec celery -A LogisticsCore worker --loglevel=info --concurrency=${CELERY_CONCURRENCY:-2}
