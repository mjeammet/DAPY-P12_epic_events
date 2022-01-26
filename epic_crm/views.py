from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet

from epic_crm.models import User, Client, Contract, Event
from epic_crm.serializers import UserListSerializer, UserDetailSerializer, ClientListSerializer, ClientDetailSerializer, ContractSerializer, EventSerializer
from epic_crm.permissions import IsAdmin



class UserViewset(ModelViewSet):

    serializer_class = UserListSerializer
    detail_serializer_class = UserDetailSerializer
    permission_classes = (IsAdmin, )

    def get_queryset(self):
        queryset = User.objects.all()
        return queryset

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return self.detail_serializer_class
        return super().get_serializer_class()


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


class EventViewset(ModelViewSet):

    serializer_class = EventSerializer

    def get_queryset(self):
        queryset = Event.objects.all()
        return queryset
