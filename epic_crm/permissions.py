from django.contrib.auth.models import Group
from rest_framework.permissions import BasePermission

from epic_crm.models import User


class IsAdmin(BasePermission):

    def has_permission(self, request, view):
        user = request.user

        if user.is_superuser:
            return True


class IsAdminOrSales(BasePermission):

    def has_permission(self, request, view):
        user = request.user

        if user.is_superuser or Group.objects.get(name='sales') in user.groups.all():
            return True


class IsAdminOrSupport(BasePermission):

    def has_permission(self, request, view):
        user = request.user

        if user.is_superuser or Group.objects.get(name='support') in user.groups.all():
            return True