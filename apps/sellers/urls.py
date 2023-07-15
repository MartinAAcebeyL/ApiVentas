from django.urls import path
from .views import CreateSellerView

urlpatterns = [
    path('create/', CreateSellerView.as_view(), name='create_seller'),
]
