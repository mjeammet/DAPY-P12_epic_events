from django.urls import path, include
from . import views

from rest_framework import routers

from .views import ClientViewset

router = routers.SimpleRouter()
router.register('client', ClientViewset, basename='clients')

urlpatterns = [
    path('auth/', include('rest_framework.urls')),
    path('', include(router.urls)),
]