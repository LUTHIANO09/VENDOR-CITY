from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from accounts.decorators import role_required
from vendors.models import Vendor
from django.utils import timezone
from datetime import timedelta


@login_required
@role_required('compliance_officer', 'senior_management')
def compliance_dashboard(request):
    today = timezone.now().date()
    soon = today + timedelta(days=90)

    expired_vendors = Vendor.objects.filter(
        certificate_expiry__lt=today
    ).order_by('certificate_expiry')

    expiring_soon = Vendor.objects.filter(
        certificate_expiry__gte=today,
        certificate_expiry__lte=soon
    ).order_by('certificate_expiry')

    suspended_vendors = Vendor.objects.filter(status='suspended')

    context = {
        'expired_vendors': expired_vendors,
        'expiring_soon': expiring_soon,
        'suspended_vendors': suspended_vendors,
        'expired_count': expired_vendors.count(),
        'expiring_soon_count': expiring_soon.count(),
        'suspended_count': suspended_vendors.count(),
        'today': today,
    }
    return render(request, 'compliance/compliance_dashboard.html', context)


@login_required
@role_required('compliance_officer', 'senior_management')
def compliance_vendor_detail(request, pk):
    vendor = get_object_or_404(Vendor, pk=pk)
    today = timezone.now().date()
    context = {
        'vendor': vendor,
        'today': today,
    }
    return render(request, 'compliance/compliance_vendor_detail.html', context)