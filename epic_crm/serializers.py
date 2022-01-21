from rest_framework.serializers import ModelSerializer
from .models import Client, Contract, Event

class ClientListSerializer(ModelSerializer):

    class Meta:
        model = Client
        fields = ['id', 'first_name', 'last_name', 'company']


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
