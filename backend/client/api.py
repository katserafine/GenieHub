from client.models import Client
from rest_framework import viewsets, permissions
from .serializers import ClientSerializer

# Client viewset

class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = ClientSerializer