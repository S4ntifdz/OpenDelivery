from uuid import UUID
from typing import Optional

from ninja import Schema


class VehicleIn(Schema):
    type: str
    capacity_weight: float = 0
    capacity_volume: float = 0


class VehicleOut(Schema):
    uuid: UUID
    type: str
    capacity_weight: float
    capacity_volume: float


class CourierIn(Schema):
    name: str
    phone: str
    vehicle_uuid: Optional[UUID] = None


class CourierOut(Schema):
    uuid: UUID
    name: str
    phone: str
    status: str
    vehicle: Optional[VehicleOut] = None
