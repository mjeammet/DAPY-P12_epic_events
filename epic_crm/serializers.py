from django.contrib.auth.hashers import make_password
from rest_framework.serializers import ModelSerializer, ValidationError
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


class EventListSerializer(ModelSerializer):

    class Meta:
        model = Event
        fields = ['id', 'event_status', 'client']

    # def validate_event_date(self, value):
    # TODO asegurarse que el evento es en el futuro


class EventDetailSerializer(ModelSerializer):

    class Meta:
        model = Event
        fields = '__all__'
