from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import CreateSellerView, ShowSalesView, ShowSalesBySellerView

urlpatterns = [
    path("login", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("create/", CreateSellerView.as_view(), name="create_seller"),
    path("sales/", ShowSalesView.as_view(), name="show_sales"),
    path(
        "me/sales",
        ShowSalesBySellerView.as_view(),
        name="show_sales_by_seller",
    ),
]
