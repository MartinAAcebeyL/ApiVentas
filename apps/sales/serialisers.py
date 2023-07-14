from rest_framework import serializers
from .models import Sale, SaleDetail
from apps.products.models import Product


class SaleDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = SaleDetail
        fields = ['quantity', 'total', 'payment_method']
        read_only_fields = ['unit_price', 'sale']

    def create(self, validated_data):
        validated_data['sale'] = self.context['sale']
        validated_data['unit_price'] = validated_data['total'] / \
            validated_data['quantity']

        sale_detail = SaleDetail.objects.create(**validated_data)
        return sale_detail


class SaleSerializer(serializers.ModelSerializer):
    sale_detail = SaleDetailSerializer()
    product = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all())

    class Meta:
        model = Sale
        fields = '__all__'
