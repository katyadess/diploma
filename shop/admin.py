from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'parent']
    prepopulated_fields = {'slug': ('name',)}
admin.site.register(Category, CategoryAdmin)


class BrandAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}
admin.site.register(Brand, BrandAdmin)


class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'price_new', 'stock', 'is_available', 'created_at', 'updated_at']
    list_filter = ['is_available', 'created_at', 'updated_at']
    list_editable = ['price', 'price_new', 'stock', 'is_available']
    prepopulated_fields = {'slug': ('name',)}
admin.site.register(Product, ProductAdmin)


class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'rating']
admin.site.register(ProductReview, ProductReviewAdmin)

class AddressAdmin(admin.ModelAdmin):
    list_display = ['user', 'city', 'street']
admin.site.register(Address, AddressAdmin)
admin.site.register(Subscriber)



class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']
    
    
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'address', 'paid', 'created', 'updated']
    list_filter = ['paid', 'created']
    list_editable = ['paid']
    inlines = [OrderItemInline]
    

admin.site.register(Order, OrderAdmin)
admin.site.register(UserData)
admin.site.register(WishList)
admin.site.register(ReviewImage)