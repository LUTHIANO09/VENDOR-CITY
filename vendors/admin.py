from django.contrib import admin
from .models import Vendor

# Register Vendor model with custom admin display
@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):

    # Columns shown in the vendor list
    list_display = [
        'company_name',
        'registration_number',
        'email',
        'phone',
        'services_offered',
        'status',
        'rating',
        'certificate_expiry',
        'is_certificate_expired',
        'date_registered',
    ]

    # Enable search by these fields
    search_fields = ['company_name', 'email', 'registration_number', 'services_offered']

    # Filter sidebar
    list_filter = ['status', 'rating']

    # Order in admin
    ordering = ['-date_registered']