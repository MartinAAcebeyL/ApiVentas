from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework import status

from django.template.loader import get_template
from django.http import HttpResponse

from datetime import datetime
from xhtml2pdf import pisa

from .serialisers import SaleDetailSerializer
from apps.sales.models import SaleDetail, Shipment
from apps.products.models import Category, Stock
from .utils import link_callback


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


class MakePDFReportSaleView(APIView):
    # permission_classes = (permissions.IsAdminUser,)

    def get(self, request):
        # get the query params from the request
        now = datetime.today()
        start_date = request.query_params.get('start_date', '2022-01-01')
        end_date = request.query_params.get(
            'end_date', now.strftime('%Y-%m-%d'))

        # we check the dates
        try:
            start_date = datetime.strptime(start_date, '%Y-%m-%d')
            end_date = datetime.strptime(end_date, '%Y-%m-%d')

            if start_date > end_date or end_date > now:
                return Response({'message': 'Dates are wrong'},
                                status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print("error: ", e)
            return Response({'message': 'Invalid dates'},
                            status=status.HTTP_400_BAD_REQUEST)

        template_path = 'sales_report.html'
        applicants_name = "NOMBRE DEL SOLICITANTE"
        date = now.strftime('%d-%m-%Y')

        sales = SaleDetail.get_total_price_between_dates(
            start_date, end_date)

        all_categories_group_by_name = [
            category for category in
            Category.objects.values('name')
        ]

        for index, category in enumerate(all_categories_group_by_name):
            category_name = category.get('name')

            # get important data like total sales by category, total shipment cost and products, this to add to principal dictionary
            list_products = SaleDetail.     get_sale_details_between_dates_and_category(
                category_name, start_date, end_date)
            total_sales_by_category = SaleDetail.get_total_price_between_dates_and_category(
                category_name, start_date, end_date)
            total_shipment_cost_by_category = Shipment.get_shipment_cost_between_dates_and_category(
                category_name, start_date, end_date)
            current_quantity, quantity = Stock.get_current_quantity_by_product_category(
                category_name)

            # add some data to principal dictionary
            all_categories_group_by_name[index]['total_sales'] = total_sales_by_category
            all_categories_group_by_name[index]['total_shipment_cost'] = total_shipment_cost_by_category
            all_categories_group_by_name[index]['current_quantity'] = current_quantity
            all_categories_group_by_name[index]['quantity'] = quantity

            for index_1, product in enumerate(list_products):
                sale = product.get('sale')
                shipment_destination = Shipment.get_shipment_by_sale(sale)
                list_products[index_1]['destination'] = shipment_destination[0].get(
                    'destination')
                list_products[index_1]['shipping_cost'] = shipment_destination[0].get(
                    'shipping_cost')

            all_categories_group_by_name[index]['products'] = list_products

        context = {
            'nombre_solicitante': applicants_name,
            'start_date': start_date.strftime("%Y-%m-%d"),
            'end_date': end_date.strftime("%Y-%m-%d"),
            'date': date,
            'sales': sales,
            'categories': all_categories_group_by_name,
        }

        # Create a Django response object, and specify content_type as pdf
        report_name = f"InformeVentas_{datetime.now().strftime('%m-%d-%Y')}"
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{report_name}.pdf"'
        # find the template and render it.
        template = get_template(template_path)
        html = template.render(context)

        # create a pdf
        pisa_status = pisa.CreatePDF(
            html, dest=response, link_callback=link_callback)
        # if error then show some funny view
        if pisa_status.err:
            return Response('Something went wrong', status=pisa_status.err)
        return response
