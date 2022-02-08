from django.contrib.auth.models import Group
from django.shortcuts import get_object_or_404
from rest_framework.permissions import BasePermission
from rest_framework.exceptions import APIException

from epic_crm.models import User, Client


class IsAdmin(BasePermission):

    def has_permission(self, request, view):
        user = request.user

        if user.is_superuser:
            return True


class IsSalesContact(BasePermission):

    def has_permission(self, request, view):
        user = request.user
        kwargs = view.kwargs

        if user.groups.filter(name="sales").exists():
            # if view.action == "create" and request.path_info == "/api/v1/events/":
            #     # Sales team can create events for their clients
            #     client = Client.objects.filter(pk=request.data.get("client"))
            #     if not client.exists():
            #         raise APIException("Client must be an existing client id")
            #     if client.first().sales_contact == user:
            #         return True
            # else:
                # For everything else, user needs to be client sales_contact
            if view.action in ["list", "create"]:
                return True
            elif kwargs.get('pk'):
                client = get_object_or_404(Client, pk=kwargs.get('pk'))
                if client.sales_contact in [request.user, None]:
                    return True
                

    def has_object_permission(self, request, view, obj):
    
        if view.action != "destroy" and obj.sales_contact in [request.user, None]:
            print(f'\n{obj.sales_contact} {request.user}')
            return True


class IsSupportContact(BasePermission):

    def has_permission(self, request, view):
        user = request.user

        if Group.objects.get(name='support') in user.groups.all():
            return True

    def has_object_permission(self, request, view, obj):

        supportteam_allowed_actions = ['list', 'retrieve', 'update']
        if obj.support_contact == request.user and view.action in supportteam_allowed_actions:
            return True
