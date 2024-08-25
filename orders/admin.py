from django.contrib import admin
from .models import *
# Register your models here.

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']
    
    
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'address', 'paid', 'created', 'updated']
    list_filter = ['paid', 'created']
    list_editable = ['paid']
    inlines = [OrderItemInline]
    

admin.site.register(Order, OrderAdmin)