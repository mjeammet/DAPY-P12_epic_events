from django.shortcuts import render
from django.db.models import Q
from django.contrib.auth.models import Group
from rest_framework.viewsets import ModelViewSet
from rest_framework.exceptions import APIException
from rest_framework.response import Response

from epic_crm.models import User, Client, Contract, Event
from epic_crm.serializers import UserListSerializer, UserDetailSerializer, ClientListSerializer, ClientDetailSerializer, ContractListSerializer, ContractDetailSerializer, EventSerializer
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

    # def perform_update():
        # TODO handle change of group
        # my_group = Group.objects.get(name='my_group_name') 
        # my_group.user_set.add(your_user)


class ClientViewset(ModelViewSet):

    serializer_class = ClientListSerializer
    detail_serializer_class = ClientDetailSerializer
    filterset_class = ClientFilter

    def get_queryset(self):
        user = self.request.user

        if user.is_superuser:
            queryset = Client.objects.all()
        elif Group.objects.get(name='sales') in user.groups.all():
            queryset = Client.objects.filter(Q(sales_contact=user) | Q(sales_contact__isnull=True))
        elif Group.objects.get(name='support') in user.groups.all():
            queryset = Client.objects.filter(events__user=user)
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
    permission_classes = (IsAdminOrSales, )
    filterset_class = ContractFilter

    #TODO vérifier que tout fonctionne bien, en list et en retrieve, quon a bien les contrats qu'on veut
    def get_queryset(self):
        client = get_object_or_404(Client, pk=self.kwargs['client_pk'])
        queryset = Contract.objects.filter(client=client)

        return queryset

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return self.detail_serializer_class
        return super().get_serializer_class()

    def create(self, request, client_pk):
        data = request.data.copy()
        data['client'] = client_pk
        data['sales_contact'] = request.user.id

        serialized_data = ContractDetailSerializer(data=data)
        serialized_data.is_valid(raise_exception=True)
        serialized_data.save()

        return Response(serialized_data.data, status=status.HTTP_201_CREATED)


class EventViewset(ModelViewSet):

    serializer_class = EventSerializer
    permission_classes = (IsAdminOrSupport, )
    filterset_class = EventFilter

    def get_queryset(self):
        queryset = Event.objects.all()

        return queryset

# TODO paginer les résultats