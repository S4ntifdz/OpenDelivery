# LogisticsCore

> [!NOTE]
> **LogisticsCore** was originally developed as a core component of a private production delivery system. It has been open-sourced to provide a robust, modular foundation for anyone building logistics and delivery platforms.

[![Django](https://img.shields.io/badge/Django-5.2-092E20?logo=django&logoColor=white)](https://www.djangoproject.com/)
[![Django Ninja](https://img.shields.io/badge/Django%20Ninja-1.6.0-009688?logo=python&logoColor=white)](https://django-ninja.rest-framework.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**LogisticsCore** is a high-performance, modular monolith designed to manage complex delivery operations. Built with **Django 5.2** and **Django Ninja**, it provides a robust API for multi-tenant logistics services, courier integrations, and real-time shipment tracking.

---

## 🌎 Internationalization

- [Español (Spanish)](i18n/spanish/README.md)

---

## ✨ Key Features

- 🏢 **Multi-tenant Architecture**: Isolated data and configurations for different logistics clients.
- 📦 **Modular Monolith**: Clean separation of concerns (Orders, Shipments, Pricing, Providers, Routing).
- 🚚 **Courier Integrations**: Seamlessly connect with multiple shipping providers via a modular Strategy pattern.
- ⚡ **Asynchronous Processing**: Powered by **Celery** and **Redis** for heavy background tasks.
- 🛠️ **Modern Admin Interface**: Premium dashboard experience using **Django Unfold**.
- 🔐 **API First**: Fully documented RESTful API with **Swagger/OpenAPI** integration.

---

## 🏗️ System Architecture

LogisticsCore follows a **Modular Monolith** pattern. Each domain is an independent Django app with its own logic:

- `shipments/`: Core shipment lifecycle (Creation → Delivery).
- `providers/`: External communication gateway using the **Strategy Pattern**.
- `tenants/`: Management of different commerce clients and their configurations.
- `tracking/`: Real-time event log for shipments.
- `routing/`: Advanced route optimization (Routes → Stops → Tasks).

---

## 🚀 Quick Setup

### 1. Requirements
Ensure you have the following installed:
- Python 3.10+
- Docker & Docker Compose

### 2. Environment Configuration
Copy the template and adjust your settings:
```bash
cp .env.example .env
```

### 3. Infrastructure Initialization
Start the database and Redis services:
```bash
docker compose up -d
```

### 4. Install Dependencies
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 5. Run Migrations
```bash
python manage.py migrate
```

### 6. Create Superuser
To access the premium admin panel:
```bash
python manage.py createsuperuser
```

### 7. Start the Application
```bash
python manage.py runserver
```

---

## 🛠️ Extending the System

### Adding a New Shipping Provider
The system uses a **Strategy Pattern** to integrate external services without modifying core logic.

1. **Implement the Interface**: Create a new class in `providers/implementations/` inheriting from `ShippingProvider`.
2. **Register it**: Add your provider to the `ProviderType` choices in `shipments/enums/provider_type.py` and register it in `providers/factories/provider_factory.py`.
3. **Template**: Check `providers/implementations/example_provider.py` for a detailed implementation guide.

### Customizing the Admin (Unfold)
We use [Django Unfold](https://github.com/unfoldadmin/django-unfold) for a modern UI. To create a new admin view:

```python
from unfold.admin import ModelAdmin
from django.contrib import admin
from .models import MyModel

@admin.register(MyModel)
class MyModelAdmin(ModelAdmin):
    pass
```
Configuration for sidebar and dashboard can be found in `LogisticsCore/settings.py` under the `UNFOLD` dictionary.

---

## 📖 API & Documentation

| Portal | URL |
|---------|-----|
| **Interactive API Docs** | `http://localhost:8000/api/v1/docs` |
| **Django Admin** | `http://localhost:8000/admin/` |

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
