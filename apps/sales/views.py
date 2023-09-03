from rest_framework.views import APIView
from rest_framework import permissions
from .serialisers import SaleDetailSerializer
from rest_framework.response import Response
from rest_framework import status
from django.template.loader import get_template
from xhtml2pdf import pisa
from datetime import datetime


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
    permission_classes = (permissions.IsAdminUser,)

    def get(self, request):
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')

        try:
            start_date = datetime.strptime(start_date, '%Y-%m-%d')
            end_date = datetime.strptime(end_date, '%Y-%m-%d')
            if start_date > end_date:
                return Response({'message': 'Start date must be before end date'}, status=status.HTTP_400_BAD_REQUEST)
        except ValueError:
            return Response({'message': 'Invalid datses'}, status=status.HTTP_400_BAD_REQUEST)

        template_path = 'user_printer.html'
        context = {'myvar': 'this is your template context'}
        # Create a Django response object, and specify content_type as pdf
        response = Response(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="report.pdf"'
        # find the template and render it.
        template = get_template(template_path)
        html = template.render(context)

        # create a pdf
        pisa_status = pisa.CreatePDF(html, dest=response)
        # if error then show some funny view
        if pisa_status.err:
            return Response('We had some errors <pre>' + html + '</pre>')
        return response
