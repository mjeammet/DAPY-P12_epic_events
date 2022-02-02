from django.contrib.auth.models import Group
from django.shortcuts import get_object_or_404
from rest_framework.permissions import BasePermission

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

        if Group.objects.get(name='sales') in user.groups.all():

            if view.action == "list" and "client_pk" not in view.kwargs:
                return True
            else:
                client_id = kwargs['client_pk'] if 'client_pk' in kwargs else kwargs['pk'] if 'pk' in kwargs else None
                client = get_object_or_404(Client, pk=client_id)

                if client.sales_contact in [request.user, None]:
                    return True
                

    # def has_object_permission(self, request, view, obj):
    #     pass

class IsAdminOrSupport(BasePermission):

    def has_permission(self, request, view):
        user = request.user

        if user.is_superuser or Group.objects.get(name='support') in user.groups.all():
            return True