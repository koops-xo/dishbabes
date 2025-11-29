from django.urls import path
from .views import dishwasher

urlpatterns = [
    path("", dishwasher, name="dishwasher"),
]
