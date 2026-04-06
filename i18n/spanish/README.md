# LogisticsCore

> [!NOTE]
> **LogisticsCore** fue desarrollado originalmente como un componente central de un sistema de delivery privado en producción. Se ha liberado como código abierto para proporcionar una base robusta y modular a cualquiera que esté construyendo plataformas de logística y entrega.

[![Django](https://img.shields.io/badge/Django-5.2-092E20?logo=django&logoColor=white)](https://www.djangoproject.com/)
[![Django Ninja](https://img.shields.io/badge/Django%20Ninja-1.6.0-009688?logo=python&logoColor=white)](https://django-ninja.rest-framework.com/)
[![Licencia: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**LogisticsCore** es un monolito modular de alto rendimiento diseñado para gestionar operaciones de entrega complejas. Construido con **Django 5.2** y **Django Ninja**, proporciona una API robusta para servicios de logística multi-tenant, integraciones de mensajería y seguimiento de envíos en tiempo real.

---

## 🌎 Internacionalización

- [English (Inglés)](../../README.md)

---

## ✨ Características Principales

- 🏢 **Arquitectura Multi-tenant**: Aislamiento de datos y configuraciones para diferentes clientes logísticos.
- 📦 **Monolito Modular**: Separación limpia de responsabilidades (Pedidos, Envíos, Precios, Proveedores, Rutas).
- 🚚 **Integraciones de Mensajería**: Conexión fluida con múltiples proveedores de envío mediante un patrón de diseño **Strategy** modular.
- ⚡ **Procesamiento Asíncrono**: Impulsado por **Celery** y **Redis** para tareas pesadas en segundo plano.
- 🛠️ **Interfaz de Administración Moderna**: Experiencia de dashboard premium utilizando **Django Unfold**.
- 🔐 **API First**: API RESTful completamente documentada con integración **Swagger/OpenAPI**.

---

## 🏗️ Arquitectura del Sistema

LogisticsCore sigue un patrón de **Monolito Modular**. Cada dominio es una aplicación Django independiente con su propia lógica:

- `shipments/`: Ciclo de vida central del envío (Creación → Entrega).
- `providers/`: Pasarela de comunicación externa mediante el patrón **Strategy**.
- `tenants/`: Gestión de diferentes clientes comerciales y sus configuraciones.
- `tracking/`: Registro de eventos en tiempo real para los envíos.
- `routing/`: Optimización avanzada de rutas (Rutas → Paradas → Tareas).

---

## 🚀 Configuración Rápida

### 1. Requisitos
Asegúrate de tener instalado:
- Python 3.10+
- Docker & Docker Compose

### 2. Configuración del Entorno
Copia la plantilla y ajusta tus configuraciones:
```bash
cp .env.example .env
```

### 3. Inicialización de la Infraestructura
Inicia los servicios de base de datos y Redis:
```bash
docker compose up -d
```

### 4. Instalar Dependencias
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 5. Ejecutar Migraciones
```bash
python manage.py migrate
```

### 6. Crear Superusuario
Para acceder al panel de administración premium:
```bash
python manage.py createsuperuser
```

### 7. Iniciar la Aplicación
```bash
python manage.py runserver
```

---

## 🛠️ Extendiendo el Sistema

### Añadir un Nuevo Proveedor de Envío
El sistema utiliza un patrón **Strategy** para integrar servicios externos sin modificar la lógica central.

1. **Implementar la Interfaz**: Crea una nueva clase en `providers/implementations/` que herede de `ShippingProvider`.
2. **Registrarlo**: Añade tu proveedor a las opciones de `ProviderType` en `shipments/enums/provider_type.py` y regístralo en `providers/factories/provider_factory.py`.
3. **Plantilla**: Consulta `providers/implementations/example_provider.py` para una guía detallada de implementación.

### Personalizar la Administración (Unfold)
Utilizamos [Django Unfold](https://github.com/unfoldadmin/django-unfold) para una interfaz moderna. Para crear una nueva vista de administración:

```python
from unfold.admin import ModelAdmin
from django.contrib import admin
from .models import MyModel

@admin.register(MyModel)
class MyModelAdmin(ModelAdmin):
    pass
```
La configuración de la barra lateral y el dashboard se encuentra en `LogisticsCore/settings.py` bajo el diccionario `UNFOLD`.

---

## 📖 API y Documentación

| Portal | URL |
|---------|-----|
| **Documentación Interactiva (API)** | `http://localhost:8000/api/v1/docs` |
| **Administración Django** | `http://localhost:8000/admin/` |

---

## 📄 Licencia

Este proyecto está bajo la Licencia MIT; consulta el archivo [LICENSE](LICENSE) para más detalles.
