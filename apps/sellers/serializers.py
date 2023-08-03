from rest_framework import serializers
from .models import Seller
from apps.sales.models import SaleDetail


class SellerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seller
        fields = '__all__'


class ShowSalesSerializer(serializers.ModelSerializer):
    sale_aux = serializers.SerializerMethodField()

    class Meta:
        model = SaleDetail
        fields = ['sale_aux', 'sale', 'quantity', 'total', 'unit_price',
                  'payment_method', 'created_at', 'updated_at']

    def get_sale_aux(self, obj):
        return obj.sale.id
