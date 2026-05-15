from django.db import models
from django.utils import timezone
from django.conf import settings

STATUS_CHOICES = [
    ('pending', 'Pending'),
    ('approved', 'Approved'),
    ('suspended', 'Suspended'),
]

RATING_CHOICES = [
    (1, '1 - Very Poor'),
    (2, '2 - Poor'),
    (3, '3 - Average'),
    (4, '4 - Good'),
    (5, '5 - Excellent'),
]

class Vendor(models.Model):
    # Link to the user account
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True, blank=True,
        related_name='vendor_profile'
    )

    # Basic company information
    company_name        = models.CharField(max_length=200)
    registration_number = models.CharField(max_length=100, unique=True)
    email               = models.EmailField(unique=True)
    phone               = models.CharField(max_length=20)
    address             = models.TextField()

    # Services and status
    services_offered    = models.TextField(help_text="Describe the services this vendor provides")
    status              = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    rating              = models.IntegerField(choices=RATING_CHOICES, default=3)

    # Certificate info
    certificate_name    = models.CharField(max_length=200, blank=True, null=True)
    certificate_file    = models.FileField(upload_to='certificates/', blank=True, null=True)
    certificate_expiry  = models.DateField(blank=True, null=True)

    # Tracking
    date_registered     = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-date_registered']
        verbose_name = 'Vendor'
        verbose_name_plural = 'Vendors'

    def __str__(self):
        return f"{self.company_name} ({self.status})"

    @property
    def is_certificate_expired(self):
        if self.certificate_expiry:
            return self.certificate_expiry < timezone.now().date()
        return False