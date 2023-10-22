from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from .models import *

class CustomUserAdmin(UserAdmin):

    model = User

    list_display = ('email', 'first_name', 'last_name','is_active',
                    'is_staff', 'is_superuser', 'last_login','is_online')
    list_filter = ('is_active', 'is_staff', 'is_superuser', 'is_online')
    fieldsets = (
        (None, {'fields': ('first_name', 'last_name','email', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active',
         'is_superuser','is_online', 'groups', 'user_permissions')}),
        ('Dates', {'fields': ('last_login', 'date_joined')})
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('first_name', 'last_name', 'email', 'password1', 'password2', 'is_staff', 'is_active','is_online')}
         ),
    )
    search_fields = ('email','first_name','last_name',)
    ordering = ('email','first_name','last_name',)


class UserGroupAdmin(admin.ModelAdmin):
    model = Group

    list_display = ('name', 'group_info', 'creator','created_at',)
    list_filter = ('creator','created_at')

    search_fields = ('name','creator')
    ordering = ('name','created_at')


admin.site.register(User, CustomUserAdmin)
admin.site.register(UserGroup, UserGroupAdmin)
admin.site.register(UserProfile)
admin.site.register(UserGroupProfile)

admin.site.unregister(Group)