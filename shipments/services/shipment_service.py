import logging
from decimal import Decimal
from datetime import datetime, timedelta

from shipments.schemas import ShipmentCreateIn, ShipmentQuoteIn
from shipments.models import ShipmentQuoteModel
from shipments.repositories.shipment_repository import ShipmentRepository
from shipments.services.shipment_tasks import process_shipment_creation
from tracking.repositories.tracking_repository import TrackingRepository
from providers.factories.provider_factory import get_provider
from shipments.enums import ShipmentStatus

logger = logging.getLogger(__name__)


class ShipmentService:
    """
    Servicio principal de Dominio para Shipments.
    Orquesta persistencia atómica en bd local, llamados asíncronos y actualizaciones de estado.
    """

    @staticmethod
    def create_shipment(payload: ShipmentCreateIn, tenant=None):
        """
        Paso 1: Persiste shipment en local rápido de forma atómica.
        Paso 2: Encola la tarea de Celery para pegarle al provider en background.
        """
        # 1. Resolución del Provider (Estrategia)
        # Si el payload no trae provider (ej: Comandaya no sabe qué usa el local),
        # usamos el default que tiene configurado el Tenant (Comercio).
        if not payload.provider and tenant:
            payload.provider = tenant.default_provider
        
        if not payload.provider:
             payload.provider = "INTERNAL" # Fallback extremo

        # 1. BD Transaccional (Rápido)
        shipment = ShipmentRepository.create_from_payload(payload, tenant=tenant)

        # 2. Redis/Celery (Task Async a Internet - Lento)
        payload_dict = payload.dict()
        process_shipment_creation.delay(str(shipment.uuid), payload_dict)

        logger.info(f"Shipment {shipment.uuid} creation payload enqueued.")
        return shipment

    @staticmethod
    def get_quote(payload: ShipmentQuoteIn, tenant=None) -> ShipmentQuoteModel:
        """
        Solicita una cotización al provider y la persiste localmente.
        """
        # 1. Resolver provider - igual que en create_shipment:
        # el Tenant tiene prioridad, si no hay tenant usamos lo que manda el payload.
        if tenant and tenant.default_provider:
            provider_name = tenant.default_provider
        else:
            provider_name = payload.provider

        provider = get_provider(provider_name)

        # 2. Obtener cotización del partner (Llamada externa)
        payload_dict = payload.dict()
        logger.info(f"[ShipmentService] get_quote - provider={provider_name}, payload_dict keys={list(payload_dict.keys())}")
        logger.info(f"[ShipmentService] get_quote - origin_location={payload_dict.get('origin_location')}, destination_location={payload_dict.get('destination_location')}")
        quote_data = provider.get_quote(payload_dict)

        # 3. Persistir en BD local
        
        # Si el provider no devuelve expiración, ponemos 15 mins por defecto
        expires_at_str = quote_data.get("expires_at")
        if expires_at_str:
            expires_at = datetime.fromisoformat(expires_at_str.replace("Z", "+00:00"))
        else:
            expires_at = datetime.now() + timedelta(minutes=15)

        quote = ShipmentRepository.create_quote(
            payload=payload,
            price=Decimal(str(quote_data["price"])),
            expires_at=expires_at,
            provider_name=provider_name,
        )

        logger.info(f"Quote created for provider {provider_name}: ${quote.price}")
        return quote

    @staticmethod
    def cancel_shipment(shipment_uuid: str) -> dict:
        """ Cancela via provider y localmente. """
        shipment = ShipmentRepository.get_by_uuid(shipment_uuid)
        if not shipment:
            raise ValueError("Shipment not found")

        # Esto podría asincronizarse también si fuera lento
        provider = get_provider(shipment.provider)
        provider.cancel_shipment(str(shipment.external_id or shipment.id))

        ShipmentRepository.update_status(shipment_uuid, ShipmentStatus.CANCELLED)
        return {"success": True, "message": "Shipment cancelled successfully."}

    @staticmethod
    def get_tracking(shipment_uuid: str):
        """ Trae el último estado del provider y lo vuelca al log histórico. """
        shipment = ShipmentRepository.get_by_uuid(shipment_uuid)
        if not shipment:
            raise ValueError("Shipment not found")

        provider = get_provider(shipment.provider)
        tracking_info = provider.get_tracking(str(shipment.external_id or shipment.id))

        # Persistir el evento para observabilidad (Push emulation vía Polling)
        TrackingRepository.add_event(
            shipment=shipment,
            event_type=tracking_info.get("status_name", "UNKNOWN"),
            notes="Tracking polled from provider directly.",
        )

        return tracking_info
