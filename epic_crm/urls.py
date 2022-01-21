from django.urls import path, include
from . import views

from rest_framework_nested import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import ClientViewset, ContractViewset

router = routers.SimpleRouter()
router.register('clients', ClientViewset, basename='clients')
users_router = routers.NestedSimpleRouter(router, 'contracts', lookup='clients')
users_router.register('contracts', ContractViewset, basename='contracts')

urlpatterns = [
    path('auth/', include('rest_framework.urls')),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('', include(router.urls)),
]