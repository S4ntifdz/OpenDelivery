from django.shortcuts import render
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

from shipments.repositories.shipment_repository import ShipmentRepository
from tracking.services.tracking_service import TrackingService


def tracking_timeline_view(request):
    """
    Vista Frontend Premium para clientes.
    Muestra la barra de búsqueda y el historial inmutable de movimientos.
    """
    search_id = request.GET.get("tracking_id", "").strip()
    
    context = {
        "search_id": search_id,
        "shipment": None,
        "history": None,
        "error_message": None,
    }

    if search_id:
        # 1. Buscar el Shipment a través del Repositorio (abstractiza el Manager)
        try:
            shipment = ShipmentRepository.get_by_external_id(search_id)
            if not shipment:
                context["error_message"] = "We couldn't find a shipment with that tracking ID."
            else:
                context["shipment"] = shipment
                # 2. Extraer el timeline cronológico
                context["history"] = TrackingService.get_shipment_history(str(shipment.uuid))
        except Exception as e:
            # Captura de errores base de datos (p. ej IDs malformados)
            context["error_message"] = "The entered ID is not valid or there was a local error in the search."

    return render(request, "web/timeline.html", context)
