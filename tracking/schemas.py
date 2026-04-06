from uuid import UUID
from datetime import datetime
from typing import Optional

from ninja import Schema


class TrackingEventIn(Schema):
    shipment_uuid: UUID
    event_type: str
    notes: str = ""
    location_uuid: Optional[UUID] = None
    source: str = ""


class TrackingEventOut(Schema):
    uuid: UUID
    event_type: str
    timestamp: datetime
    notes: str
    source: str
    shipment_uuid: UUID
