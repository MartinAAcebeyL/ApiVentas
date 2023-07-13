from rest_framework import serializers
from .models import Sale


class SaleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sale
        exclude = ['total']
        read_only_fields = ['seller']
    def create(self, validated_data):
        total = validated_data['price'] * validated_data['quantity']
        validated_data['total'] = total
        return Sale.objects.create(**validated_data)