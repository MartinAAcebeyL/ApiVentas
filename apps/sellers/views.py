from rest_framework.viewsets import generics
from .serializers import SellerSerializer

class CreateSellerView(generics.CreateAPIView):
    serializer_class = SellerSerializer