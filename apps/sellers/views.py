from rest_framework.viewsets import generics
from rest_framework.response import Response
from rest_framework import permissions
from django.utils import timezone

from .serializers import (
    SellerSerializer,
    ShowSalesSerializer,
    ShowSalesBySellerSerializer,
)
from apps.sales.models import SaleDetail

import uuid


class CreateSellerView(generics.CreateAPIView):
    serializer_class = SellerSerializer


class ShowSalesView(generics.ListAPIView):
    # permission_classes = (permissions.IsAdminUser,)
    serializer_class = ShowSalesSerializer

    def get_queryset(self):
        sort = self.request.query_params.get("sort", "ASC")
        categories = self.request.query_params.getlist("categories[]", None)
        start_date = self.request.query_params.get("start_date", None)
        finish_date = self.request.query_params.get("finish_date", None)
        seller = self.request.data.get("seller", None)
        queryset = (
            SaleDetail.objects.all().order_by("sale__product__category")
            if sort == "ASC"
            else SaleDetail.objects.all().order_by("-sale__product__category")
        )

        if categories:
            queryset = queryset.filter(sale__product__category__in=categories)
        if seller:
            seller_uuid = uuid.UUID(seller)
            queryset = queryset.filter(sale__seller__user_ptr_id=seller_uuid)
        if start_date:
            start_date = timezone.datetime.strptime(start_date, "%Y-%m-%d")
            queryset = queryset.filter(created_at__gte=start_date)
        if finish_date:
            finish_date = timezone.datetime.strptime(finish_date, "%Y-%m-%d")
            queryset = queryset.filter(created_at__lte=finish_date)

        return queryset


class ShowSalesBySellerView(generics.ListAPIView):
    permission_classes = (permissions.IsAdminUser,)
    serializer_class = ShowSalesBySellerSerializer

    def get(self, request, *args, **kwargs):
        user = self.request.user

        return Response({"message": "we're working on it"})
