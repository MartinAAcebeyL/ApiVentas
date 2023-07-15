from django.urls import path
from apps.sales.views import CreateSaleView


urlpatterns = [
    path('create/', CreateSaleView.as_view(), name='create_sale'),
    
]
