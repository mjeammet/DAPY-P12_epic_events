from django.shortcuts import render, get_object_or_404
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.contrib.auth.models import Group
from rest_framework.viewsets import ModelViewSet
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from rest_framework.decorators import action, permission_classes

from epic_crm.models import User, Client, Contract, Event
from epic_crm.permissions import IsAdmin, IsSalesContact, IsSupportContact
from epic_crm.filters import ClientFilter, ContractFilter, EventFilter
from . import serializers


class MultipleSerializerMixin:
    """Mixin to distinguish list from detail serializer."""

    detail_serializer_class = None

    def get_serializer_class(self):
        detail_serializer_actions = ['retrieve', 'update', 'partial_update', 'create', 'set_password']
        if self.action in detail_serializer_actions and self.detail_serializer_class is not None:
            # Si l'action demandée est le détail alors nous retournons le serializer de détail
            return self.detail_serializer_class
        return super().get_serializer_class()


class UserViewset(MultipleSerializerMixin, ModelViewSet):

    serializer_class = serializers.UserListSerializer
    detail_serializer_class = serializers.UserDetailSerializer
    permission_classes = (IsAdmin, )

    def get_queryset(self):
        queryset = User.objects.all()
        return queryset


class ClientViewset(MultipleSerializerMixin, ModelViewSet):

    serializer_class = serializers.ClientListSerializer
    detail_serializer_class = serializers.ClientDetailSerializer
    permission_classes = [IsAdmin|IsSalesContact]
    filterset_class = ClientFilter

    def get_queryset(self):
        user = self.request.user

        if self.action == "list" and not user.is_superuser:
            if Group.objects.get(name='sales') in user.groups.all():
                queryset = Client.objects.filter(Q(sales_contact=user) | Q(sales_contact__isnull=True))
            elif Group.objects.get(name='support') in user.groups.all():
                queryset = Client.objects.filter(events__support_contact=user)
            else:
                raise APIException('You currently don\t belong to any team, please contact an admin to be added to sales or support team.')
        else:
            queryset = Client.objects.all()

        return queryset


class ContractViewset(MultipleSerializerMixin, ModelViewSet):

    serializer_class = serializers.ContractListSerializer
    detail_serializer_class = serializers.ContractDetailSerializer
    permission_classes = [IsAdmin|IsSalesContact, ]
    filterset_class = ContractFilter

    def get_queryset(self):
        user = self.request.user

        if self.action == "list" and not user.is_superuser:
            queryset = Contract.objects.filter(sales_contact=self.request.user)
        else:
            queryset = Contract.objects.all()        

        return queryset

    def create(self, request):        
        data = request.data.copy()
        data['sales_contact'] = request.user.id

        serialized_data = serializers.ContractDetailSerializer(data=data)
        serialized_data.is_valid(raise_exception=True)
        serialized_data.save()

        client = get_object_or_404(Client, pk=serialized_data.data.get('client'))
        if client.sales_contact is None:
            client.sales_contact = request.user
            client.save()

        return Response(serialized_data.data)

    def partial_update(self, request, pk=None):
        contract = get_object_or_404(Contract, pk=pk)
        if 'is_signed' in request.data:
            print(contract.is_signed)
            if not contract.is_signed and request.data["is_signed"] == "true":
                contract_just_signed = True
                # Automatiser la création de contrat ? 

        serialized_data = serializers.ContractDetailSerializer(data=request.data)
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

    def get_permissions(self):
        if self.action == "create":
            permission_classes = [IsAdmin|IsSalesContact]
        else:
            permission_classes = self.permission_classes
        return [permission() for permission in permission_classes]
