from django.urls import path
from apps.sales.views import CreateSaleView, MakePDFReportSaleView


urlpatterns = [
    path('create/', CreateSaleView.as_view(), name='create_sale'),
    path('reports', MakePDFReportSaleView.as_view(), name='sales_report')
]
