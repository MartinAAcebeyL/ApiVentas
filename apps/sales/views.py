from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from django.template.loader import get_template
from django.db.models import Sum, Count, F
from django.http import HttpResponse
from django.utils import timezone

from utils import get_date_minus_period
from datetime import datetime
from xhtml2pdf import pisa

from apps.sales.models import SaleDetail, Shipment
from apps.products.models import Category, Stock
from .serialisers import SaleDetailSerializer
from .models import Sale, SaleDetail
from .utils import link_callback

import logging


class CreateSaleView(APIView):
    permission_classes = (permissions.IsAdminUser,)
    serializer_class = SaleDetailSerializer

    def post(self, request):
        serializer = CreateSaleView.serializer_class(data=request.data)
        if serializer.is_valid():
            products = serializer.validated_data.get("sale").get("product")

            sale = Sale.objects.create(
                seller=request.user,
            )
            sale.product.set(products)
            sale.save()

            sale_detail = SaleDetail.objects.create(
                sale=sale,
                quantity=serializer.validated_data.get("quantity"),
                payment_method=serializer.validated_data.get("payment_method"),
                unit_price=serializer.validated_data.get("unit_price"),
                total=serializer.validated_data.get("quantity")
                * serializer.validated_data.get("unit_price"),
            )
            sale_detail.save()

            return Response(
                {"message": "Sale created", "data": serializer.data},
                status=status.HTTP_201_CREATED,
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CreateGraphicReportSalesView(APIView):
    def get_sales_over_time(self):
        sales_over_time = (
            SaleDetail.objects.filter(
                created_at__range=(self.start_date, self.current_time)
            )
            .values(created_at_date=F("created_at__date"))
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

    def get(self, request, period: int, per: str):
        self.start_date = get_date_minus_period(period, per)
        self.current_time = timezone.now()

        try:
            sales_over_time = self.get_sales_over_time()
            sales_by_category = self.get_sales_by_categories()
            sales_by_product = self.get_sales_by_products()
            count_payment_method_usage = self.count_payment_method_usage()

            data = {
                "sales_over_time": sales_over_time,
                "sales_by_category": sales_by_category,
                "sales_by_product": sales_by_product,
                "count_payment_method_usage": count_payment_method_usage,
            }

            return Response(
                {"message": "Data returned", "data": data}, status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {"message": "Something went wrong", "error": e.message, "data": []},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class MakePDFReportSaleView(APIView):
    """View to generate a PDF as a report"""

    permission_classes = (permissions.IsAdminUser,)

    def get(self, request):
        # get the query params from the request
        now = datetime.today()
        default_start_date = "2022-01-01"
        start_date = request.query_params.get("start_date", default_start_date)
        end_date = request.query_params.get("end_date", now.strftime("%Y-%m-%d"))
        # we check the dates
        try:
            start_date = datetime.strptime(start_date, "%Y-%m-%d")
            end_date = datetime.strptime(end_date, "%Y-%m-%d")

            if start_date > end_date or end_date > now:
                return Response(
                    {"message": "Dates are wrong"}, status=status.HTTP_400_BAD_REQUEST
                )
        except Exception as e:
            logging.error(f"Error: {e}")
            return Response(
                {"message": "Invalid dates"}, status=status.HTTP_400_BAD_REQUEST
            )
        template_path = "sales_report.html"
        applicants_name = request.user.first_name
        date = now.strftime("%d-%m-%Y")

        sales = SaleDetail.get_total_price_between_dates(start_date, end_date)

        all_categories_group_by_name = [
            category for category in Category.objects.values("name")
        ]

        for index, category in enumerate(all_categories_group_by_name):
            category_name = category.get("name")

            # get important data like total sales by category, total shipment cost and products, this to add to principal dictionary
            list_products = SaleDetail.get_sale_details_between_dates_and_category(
                category_name, start_date, end_date
            )
            total_sales_by_category = (
                SaleDetail.get_total_price_between_dates_and_category(
                    category_name, start_date, end_date
                )
            )
            total_shipment_cost_by_category = (
                Shipment.get_shipment_cost_between_dates_and_category(
                    category_name, start_date, end_date
                )
            )
            current_quantity, quantity = Stock.get_current_quantity_by_product_category(
                category_name
            )

            # add some data to principal dictionary
            all_categories_group_by_name[index]["total_sales"] = total_sales_by_category
            all_categories_group_by_name[index][
                "total_shipment_cost"
            ] = total_shipment_cost_by_category
            all_categories_group_by_name[index]["current_quantity"] = current_quantity
            all_categories_group_by_name[index]["quantity"] = quantity

            for index_1, product in enumerate(list_products):
                sale = product.get("sale")
                shipment_destination = Shipment.get_shipment_by_sale(sale)
                list_products[index_1]["destination"] = shipment_destination[0].get(
                    "destination"
                )
                list_products[index_1]["shipping_cost"] = shipment_destination[0].get(
                    "shipping_cost"
                )

            all_categories_group_by_name[index]["products"] = list_products

        context = {
            "nombre_solicitante": applicants_name,
            "start_date": start_date.strftime("%Y-%m-%d"),
            "end_date": end_date.strftime("%Y-%m-%d"),
            "date": date,
            "sales": sales,
            "categories": all_categories_group_by_name,
        }

        # Create a Django response object, and specify content_type as pdf
        report_name = f"InformeVentas_{datetime.now().strftime('%m-%d-%Y')}"
        response = HttpResponse(content_type="application/pdf")
        response["Content-Disposition"] = f'attachment; filename="{report_name}.pdf"'
        # find the template and render it.
        template = get_template(template_path)
        html = template.render(context)

        # create a pdf
        pisa_status = pisa.CreatePDF(html, dest=response, link_callback=link_callback)
        # if error then show some funny view
        if pisa_status.err:
            return Response("Something went wrong", status=pisa_status.err)
        return response
