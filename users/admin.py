from django.contrib import admin
from .models import *
from shop.models import UserData
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
# Register your models here.

    
class UserDataInline(admin.StackedInline):
    model = UserData
    can_delete = False
    verbose_name_plural = 'app_users'
    
class UserAdmin(BaseUserAdmin):
    inlines = (UserDataInline,)

admin.site.register(CustomUser, UserAdmin)
