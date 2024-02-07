from rest_framework import permissions, status
from rest_framework.viewsets import generics
from rest_framework.response import Response


from .serializers import (
    SellerSerializer,
    ShowSalesSerializer,
)
from apps.users.usecases import get_sales_by_user
from apps.sales.models import SaleDetail
from apps.utils.dates import format_date

import logging


class CreateSellerView(generics.CreateAPIView):
    """View to register new Seller but without admin permissions"""

    serializer_class = SellerSerializer


class ShowFilterSalesView(generics.ListAPIView):
    """View to find sales with or not filters"""

    permission_classes = (permissions.IsAdminUser,)
    serializer_class = ShowSalesSerializer

    def get_queryset(self):
        sort = self.request.query_params.get("sort", "ASC")
        categories = self.request.query_params.getlist("categories[]", None)
        start_date = self.request.query_params.get("start_date", None)
        finish_date = self.request.query_params.get("finish_date", None)
        seller = self.request.user

        queryset = (
            SaleDetail.objects.all().order_by("sale__product__category")
            if sort == "ASC"
            else SaleDetail.objects.all().order_by("-sale__product__category")
        )

        if categories:
            queryset = queryset.filter(sale__product__category__name__in=categories)
        if seller:
            queryset = queryset.filter(sale__seller=seller)
        if start_date:
            start_date = format_date(start_date, "%Y-%m-%d")
            queryset = queryset.filter(created_at__gte=start_date)
        if finish_date:
            finish_date = format_date(finish_date, "%Y-%m-%d")
            queryset = queryset.filter(created_at__lte=finish_date)
        return queryset

    def list(self, request, *args, **kwargs):
        try:
            queryset = self.get_queryset()
            serializer = self.get_serializer(queryset, many=True)
            return Response(
                {"data": serializer.data, "message": "Data retrieval successful"},
                status=200,
            )
        except Exception as e:
            logging.error(e)
            return Response(
                {"error": str(e), "message": "Something went wrong"}, status=500
            )


class ShowSalesBySellerView(generics.ListAPIView):
    """View to return sales of user authenticated"""

    permission_classes = (permissions.IsAdminUser,)

    def get(self, request, *args, **kwargs):
        user = self.request.user
        try:
            data = get_sales_by_user.get_sales_by_seller(user)
            return Response(
                {"data": data, "message": "Data successfully recovered"},
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response({"error": str(e)}, status=400)
