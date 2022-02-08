from django.shortcuts import get_object_or_404
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import Group
from rest_framework.serializers import ModelSerializer, ValidationError, CharField, ChoiceField
from .models import Client, Contract, Event, User


class UserListSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'groups']
        extra_kwargs = {'password': {'write_only': True}}


class UserDetailSerializer(ModelSerializer):

    # TODO find a way to input group names instead of ids

    class Meta:
        model = User
        fields = ['id', 'username', "password", "first_name", "last_name", "email", "is_superuser", "is_active", "date_joined", "last_login", "groups"]
        extra_kwargs = {'password': {'write_only': True}}

    def validate_password(self, value):
        """Hashes password."""
        if len(value) < 8:
            raise ValidationError('Password must be at least 8 characters')
        return make_password(value)


class ClientListSerializer(ModelSerializer):

    class Meta:
        model = Client
        fields = ['id', 'full_name', 'email', 'sales_contact']

    def validate_email(self, value):
        existing_client = Client.objects.filter(email=value)
        if existing_client.exists():
            raise ValidationError(f'email already listed in database.')
        return value


class ClientDetailSerializer(ModelSerializer):

    class Meta:
        model = Client
        fields = '__all__'


    # TODO élaborer pour qu'on voit les détails du sales_contact


class ContractListSerializer(ModelSerializer):

    class Meta:
        model = Contract
        fields = ["id", "client", "sales_contact", "is_signed"]


class ContractDetailSerializer(ModelSerializer):

    class Meta:
        model = Contract
        fields = '__all__'

    def validate(self, data):
        print('\n')
        client = data['client']
        user = data['sales_contact']
        print(client)
        print(user)
        if client.sales_contact in [user, None]:
            return data
        else:
            raise ValidationError("You cannot create a contract for a client who is not neither linked to you nor a prospect.")            


class EventListSerializer(ModelSerializer):

    class Meta:
        model = Event
        fields = ['id', 'event_status', 'client']


class EventDetailSerializer(ModelSerializer):

    class Meta:
        model = Event
        fields = '__all__'
        read_only_fields = ['client', 'support_contact']

    # def validate_event_date(self, value):
    # TODO asegurarse que el evento es en el futuro
    def validate_event_date(self, value):
        pass