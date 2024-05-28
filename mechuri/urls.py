from django.urls import path
from .views import base_views


urlpatterns = [
    path('', base_views.index),
]
