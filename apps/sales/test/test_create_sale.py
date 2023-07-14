from . import TestBase
from rest_framework import status
from apps.sales.models import Sale, SaleDetail


class TestCreateSaleView(TestBase):
    def test_create_sale(self):
        url = self.urls['create']
        data = {
            "sale": {
                "seller": self.seller.id,
                "product": [1]
            },
            "quantity": 5,
            "total": 500,
            "payment_method": "qr",
            "unit_price": 1
        }

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(SaleDetail.objects.count(), 1)
        self.assertEqual(Sale.objects.count(), 1)

        sale_detail = SaleDetail.objects.first()
        self.assertEqual(sale_detail.quantity, data['quantity'])
        self.assertEqual(sale_detail.total, data['total'])
        self.assertEqual(sale_detail.payment_method, data['payment_method'])

    def test_create_invalid_sale(self):
        url = self.urls['create']
        data = {
            'quantity': 0,
            'total': 100.00,
            'payment_method': 'cash'
        }

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(SaleDetail.objects.count(), 0)
        self.assertEqual(Sale.objects.count(), 0)
