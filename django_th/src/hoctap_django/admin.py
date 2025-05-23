from django.contrib import admin
from .models import Product
# Register your models here.
# admin.site.register(Product) Nếu muốn sử dụng admin mặt định

# list_display — những trường hiện trong bảng danh sách.

# search_fields — những trường có thể tìm kiếm.

# list_filter — những trường để tạo bộ lọc sidebar.

# ordering — thứ tự sắp xếp mặc định.

# list_per_page — số bản ghi trên 1 trang.

# readonly_fields — trường chỉ đọc (không sửa được).

# fields hoặc fieldsets — để chỉnh layout form thêm/sửa.

# inlines — để thêm các model liên quan (ForeignKey) dưới dạng inline.

# prepopulated_fields — tự động điền trường dựa trên trường khác (ví dụ slug).

# date_hierarchy — thanh lọc theo ngày.

# exclude — loại bỏ trường không muốn hiển thị.
# Tự set up lại admin 
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price') 
    search_fields = ('name',)                
    list_filter = ('price',)     
admin.site.register(Product, ProductAdmin)