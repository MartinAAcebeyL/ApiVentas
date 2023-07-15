from rest_framework import serializers
from .models import Sale, SaleDetail
from apps.products.models import Product


class SaleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sale
        fields = ['seller', 'product']


class SaleDetailSerializer(serializers.ModelSerializer):
    sale = SaleSerializer()

    class Meta:
        model = SaleDetail
        fields = ['sale', 'quantity', 'total', 'unit_price',
                  'payment_method']

    def create(self, validated_data):
        sale_data = validated_data.pop('sale')
        sale = Sale.objects.create(
            seller=sale_data['seller'],
        )
        sale.product.set(sale_data['product'])
        sale_detail = SaleDetail.objects.create(sale=sale, **validated_data)
        return sale_detail
