from rest_framework import serializers
from .models import Item, StockLog

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = '__all__'

class StockLogSerializer(serializers.ModelSerializer):
    item_name = serializers.ReadOnlyField(source='item.name')

    class Meta:
        model = StockLog
        fields = ['id', 'item', 'item_name', 'transaction_type', 'quantity', 'note', 'timestamp']
