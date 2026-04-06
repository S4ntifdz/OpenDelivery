from ninja import NinjaAPI

from LogisticsCore.api.v1.shipments_router import router as shipments_router
from LogisticsCore.api.v1.couriers_router import router as couriers_router
from LogisticsCore.api.v1.tracking_router import router as tracking_router
from LogisticsCore.api.v1.routing_router import router as routing_router
from core.security import ApiKeyAuth

api = NinjaAPI(
    title="LogisticsCore API",
    version="1.0.0",
    description="Logistics Core Delivery API",
    auth=ApiKeyAuth()
)

api.add_router("/shipments/", shipments_router, tags=["Shipments"])
api.add_router("/couriers/", couriers_router, tags=["Couriers"])
api.add_router("/tracking/", tracking_router, tags=["Tracking"])
api.add_router("/routing/", routing_router, tags=["Routing"])
