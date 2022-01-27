from django.db.models import Q
import django_filters

from epic_crm.models import Client


class ClientFilter(django_filters.FilterSet):

    email = django_filters.CharFilter(field_name="email", lookup_expr='icontains')
    name = django_filters.CharFilter(method='filter_name')

    class Meta:
        model = Client
        fields = []

    def filter_name(self, queryset, name, value):
        queryset = queryset.filter(Q(first_name__icontains=value) | Q(last_name__icontains=value))

        return queryset
