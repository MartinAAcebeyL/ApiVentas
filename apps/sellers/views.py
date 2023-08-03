from rest_framework.viewsets import generics
from rest_framework import permissions
from .serializers import SellerSerializer, ShowSalesSerializer
from apps.sales.models import SaleDetail
from datetime import datetime


class CreateSellerView(generics.CreateAPIView):
    serializer_class = SellerSerializer


class ShowSalesView(generics.ListAPIView):
    permission_classes = (permissions.IsAdminUser,)
    serializer_class = ShowSalesSerializer

    def get_queryset(self):
        sort = self.request.query_params.get('sort', 'ASC')
        categories = self.request.query_params.get('categories[]', None)
        start_date = self.request.query_params.get('start_date', None)
        finish_date = self.request.query_params.get(
            'finish_date', datetime.now().strftime('%Y-%m-%d'))
        saler = self.request.GET.get('saler', None)

        queryset = SaleDetail.objects.all().order_by(
            'sale.product.category') if sort == 'ASC' else SaleDetail.objects.all().order_by('-sale.product.category')

        if categories:
            queryset = queryset.filter(sale__product__category__in=categories)
        if saler:
            queryset = queryset.filter(sale__seller__id=saler)
        if start_date:
            queryset = queryset.filter(
                sale__created_at__range=(start_date, finish_date))

        return queryset
