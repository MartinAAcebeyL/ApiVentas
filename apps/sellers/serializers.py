from rest_framework import serializers
from .models import Seller
from apps.sales.models import SaleDetail, Sale
from apps.products.serializers import ProductSerializer
from apps.products.models import Product
from apps.sales.serialisers import SaleSerializer


class SellerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seller
        fields = "__all__"

    def create(self, validated_data):
        user = Seller(**validated_data)
        user.set_password(validated_data["password"])
        user.save()
        return user


class ShowSalesSerializer(serializers.ModelSerializer):
    sale_products = serializers.SerializerMethodField()
    sale = SaleSerializer()

    class Meta:
        model = SaleDetail
        fields = [
            "quantity",
            "total",
            "unit_price",
            "payment_method",
            "created_at",
            "updated_at",
            "sale",
            "sale_products",
        ]

    def get_sale_products(self, obj):
        sale = Sale.objects.get(id=obj.sale.id)
        try:
            product_serializer = ProductSerializer(
                Product.objects.get(id=sale.product.first().id)
            )
            return product_serializer.data
        except:
            pass


class ShowSalesBySellerSerializer(serializers.ModelSerializer):
    class Meta:
        model = SaleDetail
        fields = "__all__"

    def get_queryset(self):
        user = self.request.user
        return SaleDetail.objects.filter(sale__seller=user)

    