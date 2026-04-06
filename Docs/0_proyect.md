# 0. Arquitectura del Proyecto

## Visión General

**LogisticsCore** es un monolito modular de logística construido con Django + Django Ninja. Cada módulo del dominio es una app Django independiente con su propia API, schemas, modelos y servicios.

## Stack Tecnológico

| Componente | Tecnología |
|-----------|------------|
| Framework | Django 5.2 |
| API | Django Ninja |
| Base de datos | PostgreSQL 16 |
| ORM | Django ORM |
| Infraestructura | Docker Compose |

## Estructura de Directorios

```
LogisticsCore/
├── LogisticsCore/          ← Configuración del proyecto
│   ├── settings.py
│   ├── urls.py
│   └── api/v1/             ← API central versionada (routers)
│
├── core/                   ← Base compartida (BaseModel)
│
├── shipments/              ← Envíos, paquetes, ubicaciones, cotizaciones
├── couriers/               ← Couriers y vehículos
├── tracking/               ← Eventos de tracking
├── routing/                ← Route → Stop → Task (batching moderno)
├── providers/              ← Strategy Pattern (sin API, sin modelos)
├── tenants/                ← Gestión de Comercios (Multi-tenancy)
│
├── orders/                 ← Pedidos (por implementar)
├── pricing/                ← Pricing (por implementar)
└── dispatch/               ← Despacho (por implementar)
```

## Patrón por App

Cada app de dominio sigue esta estructura:

```
app/
├── models/                 ← Un archivo por modelo
│   ├── __init__.py         ← Exports
│   └── nombre_model.py
├── enums/                  ← Un archivo por enum (TextChoices)
│   ├── __init__.py
│   └── nombre_enum.py
├── services/               ← Lógica de negocio
│   └── __init__.py
├── schemas.py              ← Schemas de Ninja (request/response)
└── admin.py                ← Admin de Django
```

Los **routers** de cada app viven centralizados en `LogisticsCore/api/v1/`.

## Flujo de un Request

```
HTTP Request
    ↓
Django Ninja Router (api/v1/xxx_router.py)
    ↓
Schema validation (schemas.py)
    ↓
Service layer (services/)
    ↓
Models / Providers
```

**Regla de oro:** Los routers solo reciben, validan y delegan. Toda la lógica va en `services/`.

## Modelos del Dominio

### Shipments

| Modelo | Descripción |
|--------|-------------|
| `ShipmentModel` | Envío con origin/dest, proveedor, estado, precio |
| `LocationModel` | Ubicación con dirección, coordenadas, contacto |
| `PackageModel` | Paquete (peso, volumen, valor) asociado a un Shipment |
| `ShipmentQuoteModel` | Cotización de un proveedor |

### Couriers

| Modelo | Descripción |
|--------|-------------|
| `CourierModel` | Courier con nombre, teléfono, estado |
| `VehicleModel` | Vehículo con tipo y capacidades |

### Tracking

| Modelo | Descripción |
|--------|-------------|
| `TrackingEventModel` | Evento de tracking con tipo, timestamp, location, source |

### Routing (Patrón Moderno de Delivery)

| Modelo | Descripción |
|--------|-------------|
| `RouteModel` | Un viaje con múltiples paradas |
| `StopModel` | Una parada en una ubicación (con secuencia) |
| `TaskModel` | Una acción en esa parada: PICKUP o DROPOFF |

Este patrón permite **batching** (múltiples pedidos en un viaje), optimización de rutas, y es el estándar usado en Rappi, Uber, DoorDash.

### Tenants (Comercios)

| Modelo | Descripción |
|--------|-------------|
| `TenantModel` | Comercio (cliente) con API Key y estrategia por defecto |

Cada pedido en el sistema pertenece a un Tenant, lo que garantiza el aislamiento de datos y permite configurar qué carrier usa cada comercio por cuenta propia.

## 🎯 Patrón Strategy (Providers)

La app `providers/` implementa el **patrón de diseño Strategy** para desacoplar la lógica de envío de los proveedores concretos.

### Diagrama

```
┌─────────────────────────────────┐
│      ShippingProvider (ABC)     │  ← Strategy Interface
│─────────────────────────────────│
│ + create_shipment()             │
│ + cancel_shipment()             │
│ + get_tracking()                │
│ + get_quote()                   │
└───────────┬─────────────────────┘
            │ implements
    ┌───────┴───────┬───────────────┐
    │               │               │
┌───▼────┐   ┌──────▼──────────┐ ┌──▼────┐
│Example │   │InternalCourier  │ │Mock   │ ← Concrete Strategies
│Provider│   │Provider         │ │Provider│
│────────│   │─────────────────│ └───────┘
│cotizar │   │assign_courier   │
│crear   │   └─────────────────┘
│viaje   │
└────────┘

provider_factory.get_provider(type) → ShippingProvider
                                      ↑ Strategy Resolver
```

### Estructura

```
providers/
├── interfaces/
│   └── shipping_provider.py    ← Strategy Interface (ABC)
├── implementations/
│   ├── example_provider.py     ← Concrete Strategy A (template)
│   └── internal_courier_provider.py ← Concrete Strategy B
└── factories/
    └── provider_factory.py     ← Strategy Resolver (Factory)
```

### Uso

```python
from providers.factories import get_provider

# El servicio no sabe qué proveedor se usa
provider = get_provider(shipment.provider)  # → ShippingProvider
provider.create_shipment(shipment)

# Cotizar
quote = provider.get_quote(origin, destination)
```

### ¿Por qué Strategy y no un simple if/else?

1. **Open/Closed Principle**: Para agregar un nuevo proveedor (ej: Pedidos Ya), solo creás una nueva clase en `implementations/` y la registrás en la factory. No tocás código existente.
2. **Testeable**: Podés mockear `ShippingProvider` en tests sin depender de APIs externas.
3. **Desacoplado**: Los `services/` del dominio solo conocen la interfaz, nunca las implementaciones concretas.

## Enums

Cada app tiene su carpeta `enums/` con un archivo por enum:

| App | Enum | Valores |
|-----|------|---------|
| shipments | `ShipmentStatus` | CREATED, ASSIGNED, PICKED_UP, IN_TRANSIT, DELIVERED, FAILED, CANCELLED |
| shipments | `ProviderType` | EXAMPLE, INTERNAL, TEST |
| couriers | `CourierStatus` | AVAILABLE, BUSY, OFFLINE |
| tracking | `TrackingEventType` | CREATED, ASSIGNED, PICKED_UP, IN_TRANSIT, DELIVERED, FAILED |
| routing | `TaskType` | PICKUP, DROPOFF |
| routing | `RouteStatus` | PENDING, IN_PROGRESS, COMPLETED, CANCELLED |
| routing | `StopStatus` | PENDING, ARRIVED, COMPLETED, SKIPPED |
| tenants | `ProviderType` | (Igual al de shipments) |

## API Versionada

La API se versiona en `LogisticsCore/api/v1/`:

```python
# LogisticsCore/api/v1/__init__.py
api = NinjaAPI(title="LogisticsCore API", version="1.0.0")

api.add_router("/shipments/", shipments_router)
api.add_router("/couriers/", couriers_router)
api.add_router("/tracking/", tracking_router)
api.add_router("/routing/", routing_router)
```

Acceso en: `http://localhost:8000/api/v1/docs`

## Seguridad y Multi-tenancy

Toda la API está protegida con **API Key Header Authentication**.

- **Header**: `X-API-Key`
- **Lógica**: La llave identifica al `Tenant` (Comercio). Si la llave es válida, el request se asocia a ese comercio.
- **Enrutamiento Dinámico**: Si un pedido no indica `provider`, se usa el `default_provider` configurado en el `TenantModel` del comercio.

Para crear v2 en el futuro, se agrega `api/v2/` sin romper v1.
