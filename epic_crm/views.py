from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet

from epic_crm.models import Client
from epic_crm.serializers import ClientSerializer


class ClientViewset(ModelViewSet):

    serializer_class = ClientSerializer
    # permission_classes = (IsAuthenticated, IsProjectContributor, IsObjectOwner)

    def get_queryset(self):
        queryset = Client.objects.all()
        return queryset
