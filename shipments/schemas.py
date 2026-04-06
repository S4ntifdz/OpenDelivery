from uuid import UUID
from decimal import Decimal
from datetime import datetime
from typing import Optional

from ninja import Schema


from pydantic import validator

# --- Location Schemas ---

class LocationIn(Schema):
    address: str
    city: str
    postal_code: str = ""
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    contact_name: str = ""
    contact_phone: str = ""
    email: str = ""


class LocationOut(Schema):
    uuid: UUID
    address: str
    city: str
    postal_code: str
    latitude: Optional[float]
    longitude: Optional[float]
    contact_name: str
    contact_phone: str
    email: str


# --- Package Schemas ---

class PackageIn(Schema):
    weight: float = 0
    volume: float = 0
    description: str = ""
    value: Decimal = Decimal("0")


class PackageOut(Schema):
    uuid: UUID
    weight: float
    volume: float
    description: str
    value: Decimal


# --- Shipment Schemas ---

class ShipmentCreateIn(Schema):
    reference_id: str
    provider: Optional[str] = None
    quote_id: Optional[UUID] = None
    origin_location: LocationIn
    destination_location: LocationIn
    scheduled_at: Optional[datetime] = None
    preparation_time: Optional[int] = 0  # Minutos de preparación antes del pickup
    packages: list[PackageIn] = []

    @validator("destination_location")
    def validate_destination_contact(cls, v):
        if not v.contact_name or len(v.contact_name.strip()) < 2:
            raise ValueError("contact_name is required for destination and must be valid.")
        
        # Validar que no sea un email el nombre
        if "@" in v.contact_name:
            raise ValueError("contact_name cannot be an email address.")

        if not v.contact_phone or len(v.contact_phone.strip()) < 8:
            raise ValueError("contact_phone is required for destination and must be valid (min 8 chars).")
        
        if not v.email or "@" not in v.email:
            raise ValueError("email is required for destination and must be valid.")
            
        return v


class ShipmentOut(Schema):
    uuid: UUID
    reference_id: str
    provider: str
    status: str
    price: Decimal
    external_id: str
    tracking_url: str
    scheduled_at: Optional[datetime]
    created_at: datetime


# --- ShipmentQuote Schemas ---

class ShipmentQuoteIn(Schema):
    origin_location: LocationIn
    destination_location: LocationIn
    provider: Optional[str] = None  # Opcional: si no se manda, se usa el del Tenant
    preparation_time: Optional[int] = 0  # Minutos de preparación antes del pickup


class ShipmentQuoteOut(Schema):
    uuid: UUID
    price: Decimal
    provider: str
    expires_at: datetime
