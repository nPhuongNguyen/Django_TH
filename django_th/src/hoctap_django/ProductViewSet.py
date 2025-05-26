from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import viewsets
from .models import Product
from .product_serializers import ProductSerializer
from rest_framework import generics
# Sử dụng viewsets 
# class ProductViewSet(viewsets.ModelViewSet): # Tạo tất cả các hàm
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer

#Sử dụng generics
class ProductListCreateAPIView(generics.ListCreateAPIView): # Tạo hàm get, post
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    # def get_queryset(self):
    #     return Product.objects.filter(id=1)
    # def list(self, request, *args, **kwargs):
    #     queryset = self.get_queryset()
    #     serializer = ProductSerializer(queryset, many=True)
    #     return Response(serializer.data)

    

class ProductRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView): # Tạo hàm get, put, patch, delete
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class MultipleFieldLookupMixin:
    """
    Bao nhiêu lookup_feild thì phải truy vấn bấy nhiêu VD: loolup feild là ['name', 'price'] thì phải truy vấn /name/price
    """
    def get_object(self):
        queryset = self.get_queryset()             # Get the base queryset
        queryset = self.filter_queryset(queryset)  # Apply any filter backends
        filter = {}
        for field in self.lookup_fields:
            if self.kwargs.get(field): # Ignore empty fields.
                filter[field] = self.kwargs[field]
        obj = get_object_or_404(queryset, **filter)  # Lookup the object
        self.check_object_permissions(self.request, obj)
        return obj
    
class BaseRetrieveView(MultipleFieldLookupMixin, generics.RetrieveAPIView):
    pass

class BaseRetrieveUpdateDestroyView(MultipleFieldLookupMixin, generics.RetrieveUpdateDestroyAPIView):
    pass
# class RetrieveProductView(MultipleFieldLookupMixin, generics.RetrieveAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer
#     lookup_fields = ['name', 'price']

class RetrieveProductView(BaseRetrieveView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_fields = ['name', 'price']
