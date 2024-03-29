from typing import Any
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from django.template.loader import get_template
from django.http import HttpResponse
from django.utils import timezone

from apps.utils.dates import get_date_minus_period
from datetime import datetime
from xhtml2pdf import pisa

from apps.sales.usecases.create_graphic_report_usecase import CreateGraphicReportUseCase
from apps.sales.models import SaleDetail, Shipment
from apps.products.models import Category, Stock
from .serialisers import SaleDetailSerializer
from .models import Sale, SaleDetail
from .utils import link_callback
from apps.products.models import Stock


import logging
import time


class CreateSaleView(APIView):
    """View to create a new sale"""

    permission_classes = (permissions.IsAdminUser,)
    serializer_class = SaleDetailSerializer

    def post(self, request):
        start_time = time.time()
        serializer = CreateSaleView.serializer_class(data=request.data)
        if serializer.is_valid():
            quantity = serializer.validated_data.get("quantity")
            products = serializer.validated_data.get("sale").get("product")
            stock = Stock.objects.filter(product=products[0])[0]
            Stock.update_stock(id=stock.id, amount=quantity)

            sale = Sale.objects.create(
                seller=request.user,
            )
            sale.product.set(products)
            sale.save()

            sale_detail = SaleDetail.objects.create(
                sale=sale,
                quantity=quantity,
                payment_method=serializer.validated_data.get("payment_method"),
                unit_price=serializer.validated_data.get("unit_price"),
                total=quantity * serializer.validated_data.get("unit_price"),
            )
            sale_detail.save()

            end_time = time.time()
            return Response(
                {
                    "message": "Sale created",
                    "data": serializer.data,
                    "meta": {"exec_seconds": f"{(end_time - start_time):.3f}"},
                },
                status=status.HTTP_201_CREATED,
            )

        end_time = time.time()
        return Response(
            {
                "errors": serializer.errors,
                "meta": {"exec_seconds": f"{(end_time - start_time):.3f}"},
            },
            status=status.HTTP_400_BAD_REQUEST,
        )


class CreateGraphicReportSalesView(APIView):
    """View to Graphic report"""

    permission_classes = (permissions.IsAdminUser,)

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.create_graphic_report = CreateGraphicReportUseCase()

    def get(self, request, period: int, per: str):
        """
        Get graphical sales reports based on the period and time unit provided.

        Args:
        - request: Django request object.
        - period (int): Time period backwards in days.
        - per (str): Unit of time (e.g. 'days', 'weeks', 'months').

        Returns:
        - Response: Django REST Framework response object with json report data.
        """

        self.create_graphic_report.start_date = get_date_minus_period(period, per)
        self.create_graphic_report.current_time = timezone.now()
        try:
            sales_over_time = self.create_graphic_report.get_sales_over_time()
            sales_by_category = self.create_graphic_report.get_sales_by_categories()
            sales_by_product = self.create_graphic_report.get_sales_by_products()
            count_payment_method_usage = (
                self.create_graphic_report.count_payment_method_usage()
            )

            response_data = {
                "sales_over_time": sales_over_time,
                "sales_by_category": sales_by_category,
                "sales_by_product": sales_by_product,
                "count_payment_method_usage": count_payment_method_usage,
            }

            return Response(
                {"message": "Data returned ", "data": response_data},
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response(
                {"message": "Something went wrong", "error": str(e), "data": []},
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
