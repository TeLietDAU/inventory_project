from django.core.exceptions import ValidationError
from django.db import models

class Item(models.Model):
    name = models.CharField(max_length=255)
    sku = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    stock_quantity = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        db_table = 'inventory_item'

    def __str__(self):
        return f"{self.name} ({self.sku})"


class StockLog(models.Model):
    TRANSACTION_TYPES = [
        ('IN', 'Nhập kho'),
        ('OUT', 'Xuất kho'),
    ]
    
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='stock_logs')
    transaction_type = models.CharField(max_length=3, choices=TRANSACTION_TYPES)
    quantity = models.IntegerField()
    note = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'inventory_stocklog'

    def clean(self):
        if self.quantity is None or self.quantity <= 0:
            raise ValidationError({'quantity': 'Số lượng phải lớn hơn 0.'})

        if self.transaction_type == 'OUT' and self.item_id:
            current_stock = Item.objects.get(pk=self.item_id).stock_quantity
            if self.quantity > current_stock:
                raise ValidationError({'quantity': 'Số lượng xuất không được lớn hơn tồn kho hiện tại.'})

    def save(self, *args, **kwargs):
        self.full_clean()

        if not self._state.adding:
            raise ValidationError('Không được cập nhật giao dịch kho đã ghi nhận.')

        if self.transaction_type == 'IN':
            self.item.stock_quantity += self.quantity
        elif self.transaction_type == 'OUT':
            self.item.stock_quantity -= self.quantity

        self.item.save()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.transaction_type} - {self.item.name} - {self.quantity}"

