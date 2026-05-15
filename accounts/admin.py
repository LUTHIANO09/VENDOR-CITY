from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

# Register your models here.

# Register CustomUser in admin with custom display
@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):

    # Columns shown in the user list
    list_display = ['username', 'email', 'role', 'company_name', 'phone_number', 'is_active']

    # Search by these fields
    search_fields = ['username', 'email', 'company_name']

    # Filter sidebar
    list_filter = ['role', 'is_active']

    # Add role, phone, company to the edit form
    fieldsets = UserAdmin.fieldsets + (
        ('Vendor City Info', {
            'fields': ('role', 'phone_number', 'company_name')
        }),
    )