from django.urls import path
from apps.sales.views import (CreateSaleView,   CreateGraphicReportSalesView, MakePDFReportSaleView)

urlpatterns = [
    path('create/', CreateSaleView.as_view(), name='create_sale'),
    path('graphic/report/<int:period>/<str:per>/',
         CreateGraphicReportSalesView.as_view(), name='create-graphic-report'),
    path('reports', MakePDFReportSaleView.as_view(), name='sales_report')
]
