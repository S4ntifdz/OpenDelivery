from typing import Optional
from decimal import Decimal
from datetime import datetime

from django.db import transaction

from shipments.models import ShipmentModel, LocationModel, PackageModel, ShipmentQuoteModel
from shipments.schemas import ShipmentCreateIn, ShipmentQuoteIn
from tenants.services.webhook_service import WebhookService


class ShipmentRepository:
    """
    Repositorio para aislar toda la lógica de persistencia a BD de Shipments.
    """

    @staticmethod
    def create_from_payload(payload: ShipmentCreateIn, tenant=None) -> ShipmentModel:
        """
        Crea un envío y sus relaciones (origen, destino, paquetes)
        de manera atómica en la base de datos local.
        """
        with transaction.atomic():
            origin = LocationModel.objects.create(
                address=payload.origin_location.address,
                city=payload.origin_location.city,
                postal_code=payload.origin_location.postal_code,
                latitude=payload.origin_location.latitude,
                longitude=payload.origin_location.longitude,
                contact_name=payload.origin_location.contact_name,
                contact_phone=payload.origin_location.contact_phone,
                email=payload.origin_location.email,
            )

            destination = LocationModel.objects.create(
                address=payload.destination_location.address,
                city=payload.destination_location.city,
                postal_code=payload.destination_location.postal_code,
                latitude=payload.destination_location.latitude,
                longitude=payload.destination_location.longitude,
                contact_name=payload.destination_location.contact_name,
                contact_phone=payload.destination_location.contact_phone,
                email=payload.destination_location.email,
            )

            shipment = ShipmentModel.objects.create(
                reference_id=payload.reference_id,
                provider=payload.provider,
                tenant=tenant,
                origin_location=origin,
                destination_location=destination,
                scheduled_at=payload.scheduled_at,
            )
            
            # Si viene un quote_id, lo guardamos para trazabilidad (opcional en el modelo actual)
            # Nota: El modelo ShipmentModel no tiene un campo quote_id explícito por ahora.
            # Solo lo usaremos para validar el precio si hiciera falta.

            # Create packages bulk if any
            if payload.packages:
                PackageModel.objects.bulk_create([
                    PackageModel(
                        shipment=shipment,
                        weight=pkg.weight,
                        volume=pkg.volume,
                        description=pkg.description,
                        value=pkg.value,
                    )
                    for pkg in payload.packages
                ])

            return shipment

    @staticmethod
    def create_quote(payload: ShipmentQuoteIn, price: Decimal, expires_at: datetime, provider_name: str) -> ShipmentQuoteModel:
        """ Persiste una cotización en base de datos. """
        with transaction.atomic():
            origin = LocationModel.objects.create(
                address=payload.origin_location.address,
                city=payload.origin_location.city,
                postal_code=payload.origin_location.postal_code,
                latitude=payload.origin_location.latitude,
                longitude=payload.origin_location.longitude,
                contact_name=payload.origin_location.contact_name,
                contact_phone=payload.origin_location.contact_phone,
                email=payload.origin_location.email,
            )

            destination = LocationModel.objects.create(
                address=payload.destination_location.address,
                city=payload.destination_location.city,
                postal_code=payload.destination_location.postal_code,
                latitude=payload.destination_location.latitude,
                longitude=payload.destination_location.longitude,
                contact_name=payload.destination_location.contact_name,
                contact_phone=payload.destination_location.contact_phone,
                email=payload.destination_location.email,
            )

            quote = ShipmentQuoteModel.objects.create(
                price=price,
                provider=provider_name,
                expires_at=expires_at,
                origin_location=origin,
                destination_location=destination,
            )
            return quote

    @staticmethod
    def update_provider_data(shipment_uuid: str, external_id: str, tracking_url: str, new_status: str) -> ShipmentModel:
        """Actualiza la metadata provista por el partner logístico (ej: Ejemplo)."""
        shipment = ShipmentModel.objects.get(uuid=shipment_uuid)
        shipment.external_id = external_id
        shipment.tracking_url = tracking_url
        shipment.status = new_status
        shipment.save(update_fields=["external_id", "tracking_url", "status"])
        
        # Notificar al Tenant del cambio de estado y asignación
        WebhookService.notify_status_change(shipment)
        
        return shipment

    @staticmethod
    def update_status(shipment_uuid: str, new_status: str) -> ShipmentModel:
        """Actualiza únicamente el estado del envío."""
        shipment = ShipmentModel.objects.get(uuid=shipment_uuid)
        shipment.status = new_status
        shipment.save(update_fields=["status"])
        
        # Notificar al Tenant del cambio de estado
        WebhookService.notify_status_change(shipment)
        
        return shipment

    @staticmethod
    def get_by_uuid(shipment_uuid: str) -> Optional[ShipmentModel]:
        return ShipmentModel.objects.filter(uuid=shipment_uuid).first()

    @staticmethod
    def get_by_external_id(search_id: str) -> Optional[ShipmentModel]:
        """Delega la búsqueda al ShipmentManager en el modelo."""
        return ShipmentModel.objects.get_by_reference_or_external(search_id)
