# Routing App (Rutas y Nodos)

## Responsabilidad Principal
Provee la estructura de datos avanzada para organizar múltiples envíos (Shipments) en agrupaciones óptimas para los "Couriers".
Aplica el modelo moderno y preferido por sistemas como LastMile: `Route > Stop > Task`.

## Componentes y Modelos
- **Route**: Representa un "Manifiesto de Carga" o tour de un Courier para un día laboral. Asigna un vehículo y un repartidor a una secuencia de paradas.
- **Stop**: Una visita fìsica única (un destino a nivel lat/long). Si hay 3 envíos distintos para la misma torre de apartamentos de calle Córdoba 123, debe haber un único `Stop`.
- **Task**: Una acción específica que el repartidor realiza en un `Stop` (recoger un paquete, cobrar, entregar).

## Ventaja Operativa
Cualquier ruteador (como un motor de optimización de Google OR-Tools) tomará los `Shipments` sueltos y los consolidará dentro de esta app `Routing` construyendo la secuencia geométrica perfecta.
