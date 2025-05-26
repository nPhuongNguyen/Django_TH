from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    # url = serializers.CharField(source='get_absolute_url', read_only=True)
    class Meta:
        model = Product
        # fields = '__all__' #Dữ liệu trả về 
        fields = ['name', 'price']

# fields = '__all__'	Như code trên	Lấy tất cả trường của model.
# fields = ['id', 'name']	fields = ['name', 'price']	Chỉ định trường cụ thể hiển thị trong API.
# exclude = ['description']	exclude = ['price']	Loại bỏ trường không muốn hiển thị.

