from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from .models import Item, StockLog


class InventoryApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.item = Item.objects.create(
            name='Test item',
            sku='SKU-TEST',
            price='100.00',
            stock_quantity=10,
        )

    def test_health_check_returns_database_status(self):
        response = self.client.get('/api/health')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'ok')
        self.assertEqual(response.data['database'], 'connected')
        self.assertEqual(response.data['items_in_inventory'], 1)

    def test_stock_increases_inventory(self):
        response = self.client.post('/api/stock-logs/', {
            'item': self.item.id,
            'transaction_type': 'IN',
            'quantity': 5,
            'note': 'Restock',
        }, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.item.refresh_from_db()
        self.assertEqual(self.item.stock_quantity, 15)

    def test_stock_out_decreases_inventory(self):
        response = self.client.post('/api/stock-logs/', {
            'item': self.item.id,
            'transaction_type': 'OUT',
            'quantity': 4,
            'note': 'Sale',
        }, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.item.refresh_from_db()
        self.assertEqual(self.item.stock_quantity, 6)

    def test_stock_out_cannot_exceed_inventory(self):
        response = self.client.post('/api/stock-logs/', {
            'item': self.item.id,
            'transaction_type': 'OUT',
            'quantity': 11,
            'note': 'Too many',
        }, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.item.refresh_from_db()
        self.assertEqual(self.item.stock_quantity, 10)

    def test_stock_logs_are_not_editable(self):
        log = StockLog.objects.create(item=self.item, transaction_type='IN', quantity=2)

        response = self.client.patch(f'/api/stock-logs/{log.id}/', {
            'quantity': 20,
        }, format='json')

        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
