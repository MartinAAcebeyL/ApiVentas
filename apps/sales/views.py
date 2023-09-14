from rest_framework.views import APIView
from rest_framework import permissions
from .serialisers import SaleDetailSerializer
from rest_framework.response import Response
from rest_framework import status
from django.template.loader import get_template
from xhtml2pdf import pisa
from datetime import datetime
from django.http import HttpResponse
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
        end_date = request.query_params.get('end_date', '2023-01-01')

        # we check the dates
        try:
            start_date = datetime.strptime(start_date, '%Y-%m-%d')
            end_date = datetime.strptime(end_date, '%Y-%m-%d')
            if start_date > end_date:
                return Response({'message': 'Start date must be before end date'}, status=status.HTTP_400_BAD_REQUEST)
            if end_date > datetime.now():
                return Response({'message': 'End date must be before current date'}, status=status.HTTP_400_BAD_REQUEST)
        except ValueError:
            return Response({'message': 'Invalid datses'}, status=status.HTTP_400_BAD_REQUEST)

        template_path = 'sales_report.html'
        nombre_solicitante = "Juan Pérez"
        fecha = "10 de septiembre de 2023"

        start_date = "01/08/2023"
        end_date = "31/08/2023"
        date = "02/09/2023"
        sales = 1500.00

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
            'start_date': start_date,
            'end_date': end_date,
            'date': date,
            'sales': sales,
            'categories': categories,
        }

        # Create a Django response object, and specify content_type as pdf
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="report.pdf"'
        # find the template and render it.
        template = get_template(template_path)
        html = template.render(context)

        # create a pdf
        pisa_status = pisa.CreatePDF(
            html, dest=response, link_callback=link_callback)
        # if error then show some funny view
        if pisa_status.err:
            return Response('We had some errors <pre>' + html + '</pre>')
        return response
