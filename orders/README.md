# Orders App (E-Commerce)

## Responsabilidad Principal
Actúa como un proxy de pre-filtrado si este sistema tiene que consumir pedidos de un E-commerce (ej: Tienda Nube, Shopify, Magento o un POS propio).

## Concepto
A diferencia de un **Shipment** (Envío) que es la confirmación logística formal lista a ser despachada, una **Order** (Orden) puede tener información sobre productos (SKU), carritos de compra, clientes que aún no abonaron.

Si el negocio cambia de estado al pago, entonces una `Order` origina automáticamente uno o varios `Shipments`.
