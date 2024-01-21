from rest_framework import serializers
from .models import Sale, SaleDetail


class SaleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sale
        fields = ["product"]


class SaleDetailSerializer(serializers.ModelSerializer):
    sale = SaleSerializer()

    class Meta:
        model = SaleDetail
        fields = ["sale", "quantity", "unit_price", "payment_method"]
