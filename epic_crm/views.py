from django.shortcuts import render
from django.db.models import Q
from django.contrib.auth.models import Group
from rest_framework.viewsets import ModelViewSet

from epic_crm.models import User, Client, Contract, Event
from epic_crm.serializers import UserListSerializer, UserDetailSerializer, ClientListSerializer, ClientDetailSerializer, ContractSerializer, EventSerializer
from epic_crm.permissions import IsAdmin, IsAdminOrSales, IsAdminOrSupport
from epic_crm.filters import ClientFilter, ContractFilter, EventFilter


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
    filterset_class = ClientFilter

    def get_queryset(self):
        user = self.request.user

        if user.is_superuser:
            queryset = Client.objects.all()
        elif Group.objects.get(name='sales') in user.groups.all():
            queryset = Client.objects.filter(sales_contact=user)
        elif Group.objects.get(name='support') in user.groups.all():
            queryset = Client.objects.filter(events__user=user)

        return queryset

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return self.detail_serializer_class
        return super().get_serializer_class()


class ContractViewset(ModelViewSet):

    serializer_class = ContractSerializer
    permission_classes = (IsAdminOrSales, )
    filterset_class = ContractFilter

    def get_queryset(self):
        queryset = Contract.objects.all()

        return queryset


class EventViewset(ModelViewSet):

    serializer_class = EventSerializer
    permission_classes = (IsAdminOrSupport, )
    filterset_class = EventFilter

    def get_queryset(self):
        queryset = Event.objects.all()

        return queryset
