from django.db import models

class Item(models.Model):
    name = models.CharField(max_length=255)
    sku = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    stock_quantity = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

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

    def save(self, *args, **kwargs):
        # Update Item stock_quantity
        if self.transaction_type == 'IN':
            self.item.stock_quantity += self.quantity
        elif self.transaction_type == 'OUT':
            self.item.stock_quantity -= self.quantity
        
        self.item.save()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.transaction_type} - {self.item.name} - {self.quantity}"

