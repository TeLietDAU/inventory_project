from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ItemViewSet, StockLogViewSet, health_check, index

router = DefaultRouter()
router.register(r'items', ItemViewSet)
router.register(r'stock-logs', StockLogViewSet)

urlpatterns = [
    path('', index, name='index'),
    path('api/health', health_check, name='health_check'),
    path('api/', include(router.urls)),
]
