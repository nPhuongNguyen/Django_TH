from rest_framework.routers import DefaultRouter
# from .ProductViewSet import ProductViewSet
from django.urls import path

from .models import Product
from .product_serializers import ProductSerializer
from .ProductViewSet import ProductListCreateAPIView, ProductRetrieveUpdateDestroyAPIView, RetrieveProductView

#viewsetsviewsets
# router = DefaultRouter()
# router.register(r'products', ProductViewSet)

# urlpatterns = router.urls

#generics
urlpatterns = [
    # path('products/', ProductListCreateAPIView.as_view()),
    path('products/<int:pk>/', ProductRetrieveUpdateDestroyAPIView.as_view()),
    # Dành cho các trường hợp đơn giản có thể khai báo sẵn truy vấn và dữ liệu đầu ra luôn 
    path('products/', ProductListCreateAPIView.as_view(queryset=Product.objects.all(), serializer_class=ProductSerializer), name='product-list'),
    path('products/retrieve-by-fields/<str:name>/<int:price>/', RetrieveProductView.as_view()),

]
