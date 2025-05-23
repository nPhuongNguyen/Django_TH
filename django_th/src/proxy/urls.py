# filepath: d:\Django_TH\django_th\src\proxy\urls.py
from django.urls import path
from .views import proxy_api

urlpatterns = [
    path('proxy/', proxy_api),
]