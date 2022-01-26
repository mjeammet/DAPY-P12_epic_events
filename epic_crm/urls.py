from django.urls import path, include
from . import views

from rest_framework_nested import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import UserViewset, ClientViewset, ContractViewset, EventViewset

user_router = routers.SimpleRouter()
user_router.register('users', UserViewset, basename='users')
clients_router = routers.SimpleRouter()
clients_router.register('clients', ClientViewset, basename='clients')
contracts_router = routers.NestedSimpleRouter(clients_router, 'clients', lookup='client')
contracts_router.register('contracts', ContractViewset, basename='contracts')
events_router = routers.NestedSimpleRouter(clients_router, 'clients', lookup='client')
events_router.register('events', EventViewset, basename='events')

urlpatterns = [
    # path('auth/', include('rest_framework.urls')), # TODO redirects to accounts/profile. Change redirect ? Delete endpoint ? 
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('', include(user_router.urls)),
    path('', include(clients_router.urls)),
    path('', include(contracts_router.urls)),
    path('', include(events_router.urls)),
]