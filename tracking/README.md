# Tracking App (Seguimiento)

## Responsabilidad Principal
Es el módulo central para la trazabilidad. Provee el histórico inmutable ("Event Sourcing") de todo lo que le sucede a un envío desde su origen hasta la puerta del cliente.

## Componentes y Modelos
- **TrackingEvent**: Entidad que registra una transición de estado de un `Shipment`. Guarda la marca de tiempo (timestamp), el evento (`CREATED`, `IN_TRANSIT`, `DELIVERED`), notas adicionales de campo (motivo de rechazo, foto adjuntada), y la latitud/longitud en la que ocurrió el registro.

## Rol Auditivo
Al asilar los eventos de estado en una aplicación de `tracking`, garantizamos poder responder a la pregunta *"¿Dónde estaba este paquete y cuándo cruzó esa frontera?"*

Los clientes externos (o usuarios de Frontend) suelen consultar esta app directamente a la hora de verificar el ETA (Tiempo Estimado de Llegada).
