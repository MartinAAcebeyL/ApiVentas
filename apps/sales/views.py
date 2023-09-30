from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework import status

from django.template.loader import get_template
from django.http import HttpResponse
from django.db.models import Sum, Q

from datetime import datetime, timezone
from xhtml2pdf import pisa

from .serialisers import SaleDetailSerializer
from apps.sales.models import SaleDetail
from apps.products.models import Category
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
        start_date = request.query_params.get('start_date', '2022-01-01')
        end_date = request.query_params.get('end_date', '2023-09-30')

        # we check the dates
        try:
            start_date = datetime.strptime(
                start_date, '%Y-%m-%d').replace(tzinfo=timezone.utc)

            end_date = datetime.strptime(
                end_date, '%Y-%m-%d').replace(tzinfo=timezone.utc)

            if start_date > end_date or end_date > datetime.now(timezone.utc):
                return Response({'message': 'Dates are wrong'},
                                status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print("error: ", e)
            return Response({'message': 'Invalid dates'},
                            status=status.HTTP_400_BAD_REQUEST)

        template_path = 'sales_report.html'
        applicants_name = "NOMBRE DEL SOLICITANTE"
        date = datetime.now().strftime('%d-%m-%Y')

        sales = 00.00
        data_group_by_categories = SaleDetail.objects.filter(
            created_at__range=(start_date, end_date)
        ).values('sale__product__category__name').annotate(
            total_quantity=Sum('quantity'),
            total_sales=Sum('total')
        ).order_by('sale__product__category__name')

        all_categories_name = Category.objects.values('name')
        all_sale_detail = SaleDetail.objects.all()

        data_group_by_categories = [category
                                    for category in all_categories_name]
        print(data_group_by_categories)
        print(SaleDetail.get_sale_details_between_dates_and_category(
            data_group_by_categories[0]['name'], start_date, end_date))

        categories = [
            {
                'name': 'Electrónica',
                'total_price': 500.00,
                'total_shipping_cost': 50.00,
                'products': [
                    {'name': 'Teléfono', 'date': '01/08/2023', 'price': 300.00,
                        'shipping_cost': 30.00, 'destination': 'Casa'},
                    {'name': 'Tablet', 'date': '02/08/2023', 'price': 200.00,
                        'shipping_cost': 20.00, 'destination': 'Oficina'},
                ],
            },
            {
                'name': 'Ropa',
                'total_price': 600.00,
                'total_shipping_cost': 60.00,
                'products': [
                    {'name': 'Camiseta', 'date': '03/08/2023', 'price': 200.00,
                        'shipping_cost': 20.00, 'destination': 'Casa'},
                    {'name': 'Pantalón', 'date': '04/08/2023', 'price': 200.00,
                        'shipping_cost': 20.00, 'destination': 'Oficina'},
                    {'name': 'Zapatos', 'date': '05/08/2023', 'price': 200.00,
                        'shipping_cost': 20.00, 'destination': 'Oficina'},
                ],
            },
        ]
        context = {
            'nombre_solicitante': applicants_name,
            'start_date': start_date.strftime("%Y-%m-%d"),
            'end_date': end_date.strftime("%Y-%m-%d"),
            'date': date,
            'sales': sales,
            'categories': categories,
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
            return Response('We had some errors <pre>' + html + '</pre>')
        return Response({"hola": "hi"})
