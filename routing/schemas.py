from uuid import UUID
from datetime import datetime
from typing import Optional

from ninja import Schema


class StopOut(Schema):
    uuid: UUID
    sequence: int
    status: str
    arrived_at: Optional[datetime]
    completed_at: Optional[datetime]


class TaskOut(Schema):
    uuid: UUID
    type: str
    completed_at: Optional[datetime]
    notes: str


class RouteOut(Schema):
    uuid: UUID
    status: str
    estimated_distance: Optional[float]
    estimated_duration: Optional[float]
    shipment_uuid: UUID
