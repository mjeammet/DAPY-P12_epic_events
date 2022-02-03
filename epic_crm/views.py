from django.shortcuts import render, get_object_or_404
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.contrib.auth.models import Group
from rest_framework.viewsets import ModelViewSet
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from rest_framework.decorators import action, permission_classes

from epic_crm.models import User, Client, Contract, Event
from epic_crm.serializers import UserListSerializer, UserDetailSerializer, ClientListSerializer, ClientDetailSerializer, ContractListSerializer, ContractDetailSerializer
from epic_crm.permissions import IsAdmin, IsSalesContact, IsSupportContact
from epic_crm.filters import ClientFilter, ContractFilter, EventFilter
from . import serializers


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

    # def perform_update():
        # TODO handle change of group
        # my_group = Group.objects.get(name='my_group_name') 
        # my_group.user_set.add(your_user)

    # TODO ajouter fonction partial_update pour attribuer à telle ou telle équipe


class ClientViewset(ModelViewSet):

    serializer_class = ClientListSerializer
    detail_serializer_class = ClientDetailSerializer
    permission_classes = [IsAdmin|IsSalesContact|IsSupportContact]
    filterset_class = ClientFilter

    def get_queryset(self):
        user = self.request.user

        if user.is_superuser:
            queryset = Client.objects.all()
        elif Group.objects.get(name='sales') in user.groups.all():
            queryset = Client.objects.filter(Q(sales_contact=user) | Q(sales_contact__isnull=True))
        elif Group.objects.get(name='support') in user.groups.all():
            queryset = Client.objects.filter(events__support_contact=user)
        else:
            raise APIException('You currently don\t belong to any team, please contact an admin to be added to sales or support team.')

        return queryset

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return self.detail_serializer_class
        return super().get_serializer_class()


class ContractViewset(ModelViewSet):

    serializer_class = ContractListSerializer
    detail_serializer_class = ContractDetailSerializer
    permission_classes = [IsAdmin|IsSalesContact, ]
    filterset_class = ContractFilter

    def get_queryset(self):
        client = get_object_or_404(Client, pk=self.kwargs['client_pk'])
        queryset = Contract.objects.filter(client=client)

        return queryset

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return self.detail_serializer_class
        return super().get_serializer_class()

    def get_permissions(self):
        if self.action == "destroy":
            permission_classes = [IsAdmin]
        else:
            permission_classes = self.permission_classes
        return [permission() for permission in permission_classes]

    def get_permissions(self):
        if self.action == "destroy":
            permission_classes = [IsAdmin]
        else:
            permission_classes = self.permission_classes
        return [permission() for permission in permission_classes]

    def create(self, request, client_pk):
        client = get_object_or_404(Client, pk=client_pk)
        
        data = request.data.copy()
        data['client'] = client_pk
        data['sales_contact'] = request.user.id

        if client.sales_contact is None:
            client.sales_contact = request.user
            # TODO test that
        serialized_data = ContractDetailSerializer(data=data)
        serialized_data.is_valid(raise_exception=True)
        serialized_data.save()        

        return Response(serialized_data.data)

    def partial_update(self, request, client_pk, pk=None):
        contract = get_object_or_404(Contract, pk=pk)
        if 'is_signed' in request.data:
            print(contract.is_signed)
            if not contract.is_signed and request.data["is_signed"] == "true":
                contract_just_signed = True
                # Automatiser la création de contrat ? 

        serialized_data = ContractDetailSerializer(data=request.data)
        serialized_data.is_valid(raise_exception=True)
        serialized_data.save()

        return Response(serialized_data.data)

    # @action(detail=True, methods=['post'])
    # def create_event(self, request, *args, **kwargs):
    #     print("this contract has been signed.")
    #     EventViewset.reverse_action()


class EventViewset(ModelViewSet):

    serializer_class = serializers.EventListSerializer
    detail_serializer_class = serializers.EventDetailSerializer
    permission_classes = [IsAdmin|IsSupportContact, ]
    filterset_class = EventFilter

    def get_queryset(self):
        user = self.request.user    
        queryset = Event.objects.filter(support_contact=user)

        return queryset

    def get_serializer_class(self):
        if self.action in ['retrieve', 'partial_update', 'create']:
            return self.detail_serializer_class
        return super().get_serializer_class()

    def get_permissions(self):
        if self.action == "create":
            permission_classes = [IsAdmin|IsSalesContact]
        elif self.action == "destroy":
            permission_classes = [IsAdmin]
        else:
            permission_classes = self.permission_classes
        return [permission() for permission in permission_classes]
