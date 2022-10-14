from django.urls import path, include
from rest_framework import routers, permissions
from rest_framework.authtoken import views

from .views import index

router = routers.DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),
]