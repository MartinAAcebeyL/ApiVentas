from rest_framework.views import APIView
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Sum, Count, F
from django.utils import timezone

from .serialisers import SaleDetailSerializer
from .models import SaleDetail
from utils import get_date_minus_period, show_query_sets


class CreateSaleView(APIView):
    # permission_classes = (permissions.IsAdminUser,)
    serializer_class = SaleDetailSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            # serializer.validated_data['seller'] = request.user.seller
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CreateGraphicReportSalesView(APIView):
    def get_sales_per_sellers(self):
        pass

    def get_sales_over_time(self):
        sales_over_time = SaleDetail.objects.filter(
            created_at__range=(self.start_date, self.current_time)
        ).values(created_at_date=F('created_at__date')).annotate(
            total_sales=Sum('total')
        ).order_by('created_at')
        return sales_over_time

    def get_sales_by_categories(self):
        sales_group_by_category = SaleDetail.objects.filter(
            created_at__range=(self.start_date, self.current_time)
        ).values(category_name=F('sale__product__category__name'))\
            .annotate(
            total_sales=Sum('total'),
            sales_count=Count('sale__id')
        )
        return sales_group_by_category

    def get_sales_by_products(self):
        product_sales = SaleDetail.objects\
            .filter(
                created_at__range=(self.start_date, self.current_time))\
            .values('sale__product__name')\
            .annotate(
                total_sales=Sum('total'),
                sales_count=Count('sale__id')
            )

        return product_sales

    def count_payment_method_usage(self):
        payment_method_count = SaleDetail.objects\
            .values('payment_method')\
            .filter(
                created_at__range=(self.start_date, self.current_time))\
            .annotate(usage_count=Count('payment_method'))

        return payment_method_count

    def get(self, request, period: int, per: str):
        self.start_date = get_date_minus_period(period, per)
        self.current_time = timezone.now()

        try:
            sales_over_time = self.get_sales_over_time()
            sales_by_category = self.get_sales_by_categories()
            sales_by_product = self.get_sales_by_products()
            count_payment_method_usage = self.count_payment_method_usage()

            data = {
                'sales_over_time': sales_over_time,
                'sales_by_category': sales_by_category,
                'sales_by_product': sales_by_product,
                'count_payment_method_usage': count_payment_method_usage
            }

            return Response({
                "message": "Data returned",
                "data": data
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                "message": "Something went wrong",
                "error": e.message,
                "data": []
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
