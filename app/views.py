import logging

from django.conf import settings
from django.db import connection
from django.shortcuts import render
from django.utils import timezone
from rest_framework import status, viewsets
from rest_framework.decorators import api_view
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from .models import Item, StockLog
from .serializers import ItemSerializer, StockLogSerializer

logger = logging.getLogger(__name__)


def index(request):
    """Serve the frontend dashboard."""
    return render(request, 'inventory/index.html', {
        'API_BASE_URL': settings.API_BASE_URL,
    })


@api_view(['GET'])
def health_check(request):
    """
    Endpoint: GET /api/health
    Verify that the API is running and the database connection is active.
    """
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")

        items_count = Item.objects.count()

        logger.info("Health check passed - system is healthy")
        return Response({
            "status": "ok",
            "message": "Inventory System is running",
            "database": "connected",
            "items_in_inventory": items_count,
            "timestamp": timezone.now().isoformat(),
        }, status=status.HTTP_200_OK)

    except Exception as exc:
        logger.error("Health check failed: %s", exc, exc_info=True)
        return Response({
            "status": "error",
            "message": "System health check failed",
            "error": str(exc),
        }, status=status.HTTP_503_SERVICE_UNAVAILABLE)


class ItemViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing inventory items.

    Endpoints:
    - GET /api/items/ - List all items
    - POST /api/items/ - Create a new item
    - GET /api/items/{id}/ - Get a specific item
    - PUT /api/items/{id}/ - Update an item
    - DELETE /api/items/{id}/ - Delete an item
    """
    queryset = Item.objects.all().order_by('-created_at')
    serializer_class = ItemSerializer

    def create(self, request, *args, **kwargs):
        try:
            name = request.data.get('name', 'Unknown')
            logger.info("Creating new product: %s", name)
            response = super().create(request, *args, **kwargs)
            logger.info("Product created successfully: %s (ID: %s)", name, response.data.get('id'))
            return response
        except Exception as exc:
            logger.error("Error creating product: %s", exc, exc_info=True)
            return Response({"error": str(exc)}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        try:
            item_id = kwargs.get('pk')
            logger.info("Deleting product ID: %s", item_id)
            response = super().destroy(request, *args, **kwargs)
            logger.info("Product deleted successfully (ID: %s)", item_id)
            return response
        except Exception as exc:
            logger.error("Error deleting product: %s", exc, exc_info=True)
            return Response({"error": str(exc)}, status=status.HTTP_400_BAD_REQUEST)


class StockLogViewSet(viewsets.ModelViewSet):
    """
    API endpoint for stock transactions.

    Stock transactions are append-only because each transaction changes the
    current stock level.
    """
    queryset = StockLog.objects.all().order_by('-timestamp')
    serializer_class = StockLogSerializer
    http_method_names = ['get', 'post', 'head', 'options']

    def create(self, request, *args, **kwargs):
        item_id = request.data.get('item')
        transaction_type = request.data.get('transaction_type')
        quantity = request.data.get('quantity')
        note = request.data.get('note', '')

        try:
            try:
                item = Item.objects.get(id=item_id)
            except Item.DoesNotExist:
                logger.warning("Item not found: ID %s", item_id)
                return Response(
                    {"error": f"Item with ID {item_id} not found"},
                    status=status.HTTP_404_NOT_FOUND,
                )

            logger.info(
                "Processing stock transaction: type=%s item=%s quantity=%s note=%s",
                transaction_type,
                item.name,
                quantity,
                note,
            )

            response = super().create(request, *args, **kwargs)

            item.refresh_from_db()
            logger.info("Stock transaction completed. New stock for %s: %s", item.name, item.stock_quantity)

            return response

        except ValidationError as exc:
            logger.warning("Invalid stock transaction: %s", exc.detail)
            return Response(exc.detail, status=status.HTTP_400_BAD_REQUEST)
        except Exception as exc:
            logger.error("Error processing stock transaction: %s", exc, exc_info=True)
            return Response({"error": str(exc)}, status=status.HTTP_400_BAD_REQUEST)
