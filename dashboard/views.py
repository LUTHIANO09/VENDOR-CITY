from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from vendors.models import Vendor
from django.utils import timezone
from datetime import timedelta


@login_required
def dashboard_home(request):
    today = timezone.now().date()
    soon = today + timedelta(days=90)

    total_vendors     = Vendor.objects.count()
    approved_vendors  = Vendor.objects.filter(status='approved').count()
    pending_vendors   = Vendor.objects.filter(status='pending').count()
    suspended_vendors = Vendor.objects.filter(status='suspended').count()
    expired_certs     = Vendor.objects.filter(certificate_expiry__lt=today).count()
    expiring_soon     = Vendor.objects.filter(
                          certificate_expiry__gte=today,
                          certificate_expiry__lte=soon
                        ).count()

    recent_vendors = Vendor.objects.all().order_by('-date_registered')[:5]
    top_vendors    = Vendor.objects.filter(status='approved').order_by('-rating')[:3]

    context = {
        'total_vendors'    : total_vendors,
        'approved_vendors' : approved_vendors,
        'pending_vendors'  : pending_vendors,
        'suspended_vendors': suspended_vendors,
        'expired_certs'    : expired_certs,
        'expiring_soon'    : expiring_soon,
        'recent_vendors'   : recent_vendors,
        'top_vendors'      : top_vendors,
        'today'            : today,
    }
    return render(request, 'dashboard/dashboard_home.html', context)