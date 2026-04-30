from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Item, StockLog
from .serializers import ItemSerializer, StockLogSerializer
import logging

logger = logging.getLogger(__name__)

def index(request):
    """
    Serve the frontend dashboard.
    """
    return render(request, 'inventory/index.html')

@api_view(['GET'])
def health_check(request):

    """
    Endpoint: GET /api/health
    Used to check if the system is running.
    """
    logger.info("Yêu cầu kiểm tra sức khỏe hệ thống")
    return Response({"status": "ok", "message": "Inventory System is running"}, status=status.HTTP_200_OK)

class ItemViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing items.
    GET /api/items/ - List items
    POST /api/items/ - Create item
    """
    queryset = Item.objects.all().order_by('-created_at')
    serializer_class = ItemSerializer

    def create(self, request, *args, **kwargs):
        logger.info(f"Đang tạo sản phẩm mới: {request.data.get('name')}")
        return super().create(request, *args, **kwargs)

class StockLogViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing stock logs (Stock In/Out).
    POST /api/stock-logs/ - Perform stock transaction
    """
    queryset = StockLog.objects.all().order_by('-timestamp')
    serializer_class = StockLogSerializer

    def create(self, request, *args, **kwargs):
        item_id = request.data.get('item')
        transaction_type = request.data.get('transaction_type')
        quantity = request.data.get('quantity')
        
        logger.info(f"Đang xử lý {transaction_type} cho sản phẩm ID {item_id}: số lượng {quantity}")
        
        # Additional validation could go here (e.g. check if stock becomes negative)
        try:
            return super().create(request, *args, **kwargs)
        except Exception as e:
            logger.error(f"Lỗi khi xử lý giao dịch kho: {str(e)}")
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

