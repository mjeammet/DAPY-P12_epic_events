from django.contrib import admin
from .models import Client, Contract, Event


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    search_fieds = ['company']


@admin.register(Contract)
class ContractAdmin(admin.ModelAdmin):
    pass


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    pass