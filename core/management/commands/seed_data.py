from django.core.management.base import BaseCommand
from django.utils import timezone
from tenants.models import TenantModel
from shipments.models import LocationModel, ShipmentModel, PackageModel
from tracking.models import TrackingEventModel
from couriers.models import CourierModel, VehicleModel
from routing.models import RouteModel, StopModel, TaskModel
from shipments.enums import ShipmentStatus, ProviderType
from tracking.enums import TrackingEventType
from couriers.enums import CourierStatus
from routing.enums import RouteStatus, StopStatus, TaskType
import uuid

class Command(BaseCommand):
    help = "Seeds the database with realistic demonstration data for Oxxo and MercadoLibre."

    def handle(self, *args, **options):
        # --- OXXO SCENARIO ---
        self.stdout.write("Seeding Oxxo demonstration data...")

        tenant_oxxo, created = TenantModel.objects.get_or_create(
            name="Oxxo",
            defaults={
                "api_key": "key_oxxo_demo_8877665544",
                "default_provider": ProviderType.TEST,
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f"Created Tenant: {tenant_oxxo.name}"))
        else:
            self.stdout.write(f"Tenant {tenant_oxxo.name} already exists.")

        # Common Hub for Oxxo
        hub_oxxo, _ = LocationModel.objects.get_or_create(
            address="Av. Constituyentes 1012, Lomas de Belmonte",
            city="Mexico City",
            defaults={
                "contact_name": "Oxxo Logistics Hub",
                "contact_phone": "+52 55 5555 1234",
            }
        )

        polanco_dest, _ = LocationModel.objects.get_or_create(
            address="Campos Elíseos 252, Polanco IV Secc",
            city="Mexico City",
            defaults={"contact_name": "Ana Maria Lopez"}
        )

        s1_oxxo, created = ShipmentModel.objects.get_or_create(
            reference_id="OXXO-DEL-101",
            tenant=tenant_oxxo,
            defaults={
                "status": ShipmentStatus.DELIVERED,
                "origin_location": hub_oxxo,
                "destination_location": polanco_dest,
                "provider": ProviderType.TEST,
            }
        )
        if created:
            TrackingEventModel.objects.create(shipment=s1_oxxo, event_type=TrackingEventType.DELIVERED, notes="Delivered successfully.")

        self.stdout.write(self.style.SUCCESS("Oxxo data seeded."))

        # --- MERCADOLIBRE ADVANCED SCENARIO ---
        self.stdout.write("\nSeeding MercadoLibre advanced scenario...")

        ml_tenant, created = TenantModel.objects.get_or_create(
            name="MercadoLibre",
            defaults={
                "api_key": "key_ml_full_demo_9988776655",
                "default_provider": ProviderType.INTERNAL,
            }
        )

        # Vehicle & Courier
        van, _ = VehicleModel.objects.get_or_create(
            type="Mercedes-Benz Sprinter",
            defaults={"capacity_weight": 1200, "capacity_volume": 10.5}
        )
        
        ml_courier, _ = CourierModel.objects.get_or_create(
            name="Marcos Galperin",
            defaults={
                "phone": "+54 11 5555 0001",
                "status": CourierStatus.BUSY,
                "vehicle": van,
            }
        )

        # Locations
        fulfillment_center, _ = LocationModel.objects.get_or_create(
            address="ML Fulfillment Center - MEX1",
            city="Tepotzotlán",
            defaults={
                "contact_name": "Warehouse Ops",
                "contact_phone": "+52 55 0000 1111",
            }
        )
        
        customer_home, _ = LocationModel.objects.get_or_create(
            address="Paseo de la Reforma 296, Juárez",
            city="Mexico City",
            defaults={
                "contact_name": "Juan Perez",
                "contact_phone": "+52 55 2222 3333",
            }
        )

        # Shipment
        ml_shipment, created = ShipmentModel.objects.get_or_create(
            reference_id="ML-ADV-001",
            tenant=ml_tenant,
            defaults={
                "status": ShipmentStatus.IN_TRANSIT,
                "origin_location": fulfillment_center,
                "destination_location": customer_home,
                "provider": ProviderType.INTERNAL,
                "price": 85.00,
                "courier": ml_courier,
            }
        )
        
        if created:
            # Package
            PackageModel.objects.create(
                shipment=ml_shipment,
                weight=2.5,
                volume=0.015,
                description="Electronics Package (PS5)",
                value=500.00
            )

            # Route
            route = RouteModel.objects.create(
                shipment=ml_shipment,
                courier=ml_courier,
                status=RouteStatus.IN_PROGRESS,
                estimated_distance=35.5,
                estimated_duration=45.0
            )

            # Stops
            stop_origin = StopModel.objects.create(
                route=route,
                location=fulfillment_center,
                sequence=1,
                status=StopStatus.COMPLETED,
                completed_at=timezone.now() - timezone.timedelta(hours=1)
            )
            
            stop_dest = StopModel.objects.create(
                route=route,
                location=customer_home,
                sequence=2,
                status=StopStatus.PENDING
            )

            # Tasks
            TaskModel.objects.create(
                stop=stop_origin,
                type=TaskType.PICKUP,
                completed_at=timezone.now() - timezone.timedelta(minutes=55),
                notes="Packages scanned and loaded into van."
            )
            
            TaskModel.objects.create(
                stop=stop_dest,
                type=TaskType.DROPOFF,
                notes="Deliver to front desk or security."
            )

            # Tracking Events
            TrackingEventModel.objects.create(
                shipment=ml_shipment,
                event_type=TrackingEventType.CREATED,
                timestamp=timezone.now() - timezone.timedelta(hours=3),
                notes="Payment confirmed. Preparing shipment.",
                source="internal"
            )
            TrackingEventModel.objects.create(
                shipment=ml_shipment,
                event_type=TrackingEventType.PICKED_UP,
                timestamp=timezone.now() - timezone.timedelta(hours=1),
                notes="Shipped from fulfillment center.",
                source="internal"
            )
            TrackingEventModel.objects.create(
                shipment=ml_shipment,
                event_type=TrackingEventType.IN_TRANSIT,
                timestamp=timezone.now() - timezone.timedelta(minutes=30),
                notes="Carrier is arriving at your location.",
                source="internal"
            )
            self.stdout.write(self.style.SUCCESS(f"MercadoLibre advanced data seeded: {ml_shipment.reference_id}"))

        self.stdout.write(self.style.SUCCESS("\nAll demo data has been successfully seeded."))
        self.stdout.write(self.style.MIGRATE_LABEL("New tracking ID: ML-ADV-001"))
