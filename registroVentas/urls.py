from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('sales/api/v1/', include('apps.sales.urls')),
    path('seller/api/v1/', include('apps.sellers.urls')),
]
