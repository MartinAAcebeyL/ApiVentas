from django.urls import path
from .views import CreateSellerView, ShowSalesView

urlpatterns = [
    path('create/', CreateSellerView.as_view(), name='create_seller'),
    path('sales/', ShowSalesView.as_view(), name='show_sales'),
]
