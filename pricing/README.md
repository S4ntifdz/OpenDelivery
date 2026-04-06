# Pricing App (Cotizaciones y Tarifas)

## Responsabilidad Principal
Centraliza la lógica de negocio y reglas que otorgan valor monetario a las operaciones logísticas.  

Si el valor de un envío depende de:
- Distancia (Cálculo OSRM / Geohash)
- Volumen (Cúbico)
- Peso
- Zona de riesgo o alta demanda (Dynamic Pricing)

Dicho cálculo vive en esta aplicación.

## Integraciones
`Shipments` y `Orders` utilizan los servicios y validadores encapsulados aquí dentro para ofrecer cotizaciones formales al cliente que desea generar un evento de entrega.
