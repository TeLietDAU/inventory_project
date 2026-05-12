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
        read_only_fields = ['id', 'item_name', 'timestamp']

    def validate_quantity(self, value):
        if value <= 0:
            raise serializers.ValidationError('Số lượng phải lớn hơn 0.')
        return value

    def validate(self, attrs):
        item = attrs.get('item')
        transaction_type = attrs.get('transaction_type')
        quantity = attrs.get('quantity')

        if item and transaction_type == 'OUT' and quantity and quantity > item.stock_quantity:
            raise serializers.ValidationError({
                'quantity': 'Số lượng xuất không được lớn hơn tồn kho hiện tại.'
            })

        return attrs
