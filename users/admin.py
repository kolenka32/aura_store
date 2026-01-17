from django.contrib import admin
from .models import CustomUser
from django.contrib.auth.admin import UserAdmin

# Register your models here.
@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ['email', 'first_name', 'last_name', 'country']
    list_filter = ['country']
    search_fields = ['email', 'first_name', 'last_name', 'country', 'city', 'company']
    ordering = ['email']
    fieldsets = [
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {
            'fields': ('image', 'first_name', 'last_name', 'company', 'address', 'city', 'country', 'province',
                       'postal_code', 'phone')
        }),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
        }),
        ('Important dates', {
            'fields': ('last_login', 'date_joined')
        }),
    ]
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', ' password1', 'password2', 'is_staff', 'is_active'),
        }),
    )

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if 'username' in form.base_fields:
            form.base_fields['username'].disabled = True

        return form
