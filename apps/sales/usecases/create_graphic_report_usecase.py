from apps.sales.models import SaleDetail
from django.db.models import Sum, Count, F


class CreateGraphicReportUseCase:
    def get_sales_over_time(self):
        sales_over_time = (
            SaleDetail.objects.filter(
                created_at__range=(self.start_date, self.current_time)
            )
            .values(created_at_date=F("created_at"))
            .annotate(total_sales=Sum("total"))
            .order_by("created_at")
        )
        return sales_over_time

    def get_sales_by_categories(self):
        sales_group_by_category = (
            SaleDetail.objects.filter(
                created_at__range=(self.start_date, self.current_time)
            )
            .values(category_name=F("sale__product__category__name"))
            .annotate(total_sales=Sum("total"), sales_count=Count("sale__id"))
        )
        return sales_group_by_category

    def get_sales_by_products(self):
        product_sales = (
            SaleDetail.objects.filter(
                created_at__range=(self.start_date, self.current_time)
            )
            .values("sale__product__name")
            .annotate(total_sales=Sum("total"), sales_count=Count("sale__id"))
        )

        return product_sales

    def count_payment_method_usage(self):
        payment_method_count = (
            SaleDetail.objects.values("payment_method")
            .filter(created_at__range=(self.start_date, self.current_time))
            .annotate(usage_count=Count("payment_method"))
        )

        return payment_method_count
