from django.contrib.auth.hashers import make_password
from rest_framework.serializers import ModelSerializer
from .models import Client, Contract, Event, User


class UserListSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'username', 'groups']

    def validate_password(self, value):
        """Hashes password."""
        if len(value) < 8:
            raise ValidationError('Password must be at least 8 characters')
        return make_password(value)


class UserDetailSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'username', "first_name", "last_name", "email", "is_superuser", "is_active", "date_joined", "last_login", "groups"]


class ClientListSerializer(ModelSerializer):

    class Meta:
        model = Client
        fields = ['id', 'first_name', 'last_name', 'email', 'sales_contact']


class ClientDetailSerializer(ModelSerializer):

    class Meta:
        model = Client
        fields = '__all__'


class ContractSerializer(ModelSerializer):

    class Meta:
        model = Contract
        fields = '__all__'


class EventSerializer(ModelSerializer):

    class Meta:
        model = Event
        fields = '__all__'
