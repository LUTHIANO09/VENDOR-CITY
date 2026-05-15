from django.db import models
from django.contrib.auth.models import AbstractUser

# We extend Django's built-in User model to add our own role field
# This is best practice - always done BEFORE first migration

class CustomUser(AbstractUser):

    # Role choices for each type of user in the system
    VENDOR_OFFICER = 'vendor_officer'
    VENDOR = 'vendor'
    COMPLIANCE_OFFICER = 'compliance_officer'
    SENIOR_MANAGEMENT = 'senior_management'

    ROLE_CHOICES = [
        (VENDOR_OFFICER, 'Vendor Officer'),
        (VENDOR, 'Vendor'),
        (COMPLIANCE_OFFICER, 'Compliance Officer'),
        (SENIOR_MANAGEMENT, 'Senior Management'),
    ]

    role = models.CharField(
        max_length=30,
        choices=ROLE_CHOICES,
        default=VENDOR,
    )

    phone_number = models.CharField(max_length=20, blank=True, null=True)
    company_name = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    # These fix the clash with Django's default auth.User
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_set',
        blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_set',
        blank=True
    )

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"

    @property
    def is_vendor(self):
        return self.role == self.VENDOR

    @property
    def is_vendor_officer(self):
        return self.role == self.VENDOR_OFFICER

    @property
    def is_compliance_officer(self):
        return self.role == self.COMPLIANCE_OFFICER

    @property
    def is_senior_management(self):
        return self.role == self.SENIOR_MANAGEMENT