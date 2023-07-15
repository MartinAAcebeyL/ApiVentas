from rest_framework.views import APIView
from rest_framework import permissions
from .serialisers import SaleDetailSerializer
from rest_framework.response import Response
from rest_framework import status


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
