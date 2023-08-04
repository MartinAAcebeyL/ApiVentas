from rest_framework import serializers
from .models import Seller
from apps.sales.models import SaleDetail, Sale
from apps.products.serializers import ProductSerializer
from apps.products.models import Product


class SellerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seller
        fields = '__all__'


class ShowSalesSerializer(serializers.ModelSerializer):
    sale_products = serializers.SerializerMethodField()

    class Meta:
        model = SaleDetail
        fields = ['sale', 'quantity', 'total', 'unit_price',
                  'payment_method', 'created_at', 'updated_at', 'sale_products']

    def get_sale_products(self, obj):
        sale = Sale.objects.get(id=obj.sale.id)
        product_serializer = ProductSerializer(
            Product.objects.get(id=sale.product.first().id))
        return product_serializer.data
