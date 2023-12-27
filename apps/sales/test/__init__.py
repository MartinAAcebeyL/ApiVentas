from django.urls import reverse
from rest_framework.test import APITestCase
from apps.sellers.models import Seller
from apps.products.management.commands.factory import create_product, create_category


class TestBase(APITestCase):
    @classmethod
    def setUpClass(cls):
        cls.urls = {
            'create': reverse('create_sale'),
        }
        cls.seller = Seller.objects.create(
            username='seller1', password='123456')

        cls.category = create_category()
        cls.product = create_product()

        super().setUpClass()
        cls.client = cls.client_class()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
