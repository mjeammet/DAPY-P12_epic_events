from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet

from epic_crm.models import Client, Contract
from epic_crm.serializers import ClientListSerializer, ClientDetailSerializer, ContractSerializer


class ClientViewset(ModelViewSet):

    serializer_class = ClientListSerializer
    detail_serializer_class = ClientDetailSerializer
    # permission_classes = (IsAuthenticated, IsProjectContributor, IsObjectOwner)

    def get_queryset(self):
        queryset = Client.objects.all()
        return queryset

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return self.detail_serializer_class
        return super().get_serializer_class()


class ContractViewset(ModelViewSet):

    serializer_class = ContractSerializer

    def get_queryset(self):
        queryset = Contract.objects.all()
        return queryset
