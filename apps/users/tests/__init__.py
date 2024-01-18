from django.urls import reverse
from rest_framework.test import APITestCase


class TestBase(APITestCase):
    @classmethod
    def setUpClass(cls):
        cls.urls = {
            'show_sales': reverse('show_sales'),
        }
        
        super().setUpClass()
        cls.client = cls.client_class()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()