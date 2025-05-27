# filepath: d:\Django_TH\django_th\src\proxy\urls.py
from django.urls import path
from .views import get_product, proxy_api

urlpatterns = [
    path('proxy/', proxy_api),
    path('api/products/<str:product_id>/', get_product, name='get_product')
]