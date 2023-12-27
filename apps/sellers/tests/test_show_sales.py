from . import TestBase
from rest_framework import status
from datetime import date
import uuid


class TestShowSales(TestBase):
    def test_filter_by_category(self):
        url = self.urls.get('show_sales')
        response = self.client.get(
            url, {'categories[]': [1, 2]})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_filter_by_seller(self):
        url = self.urls.get('show_sales')
        seller_uuid = uuid.uuid4()
        response = self.client.get(url, {'seller': seller_uuid})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_sorting(self):
        url_asc = self.urls.get('show_sales') + '?sort=ASC'
        response_asc = self.client.get(url_asc)
        self.assertEqual(response_asc.status_code, status.HTTP_200_OK)

        url_desc = self.urls.get('show_sales') + '?sort=DESC'
        response_desc = self.client.get(url_desc)
        self.assertEqual(response_desc.status_code, status.HTTP_200_OK)

    def test_filter_by_dates(self):
        url = self.urls.get('show_sales')
        start_date = '2023-07-04'
        finish_date = '2023-08-04'
        response = self.client.get(
            url, {'start_date': start_date, 'finish_date': finish_date})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
