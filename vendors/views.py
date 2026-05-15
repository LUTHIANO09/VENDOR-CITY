from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from accounts.decorators import role_required
from .models import Vendor
from django.contrib import messages


@login_required
@role_required('vendor_officer', 'senior_management', 'compliance_officer')
def vendor_list(request):
    vendors = Vendor.objects.all()
    today = timezone.now().date()
    has_expired = Vendor.objects.filter(certificate_expiry__lt=today).exists()
    context = {
        'vendors': vendors,
        'has_expired': has_expired,
    }
    return render(request, 'vendors/vendor_list.html', context)


@login_required
def vendor_detail(request, pk):
    vendor = get_object_or_404(Vendor, pk=pk)
    context = {
        'vendor': vendor,
    }
    return render(request, 'vendors/vendor_detail.html', context)


@login_required
@role_required('vendor_officer', 'senior_management', 'compliance_officer')
def vendor_approved(request):
    vendors = Vendor.objects.filter(status='approved')
    context = {
        'vendors': vendors,
        'filter_label': 'Approved Vendors',
        'has_expired': False,
    }
    return render(request, 'vendors/vendor_list.html', context)


@login_required
@role_required('vendor_officer', 'senior_management', 'compliance_officer')
def vendor_expired(request):
    today = timezone.now().date()
    vendors = Vendor.objects.filter(certificate_expiry__lt=today)
    context = {
        'vendors': vendors,
        'filter_label': 'Vendors with Expired Certificates',
        'has_expired': True,
    }
    return render(request, 'vendors/vendor_list.html', context)




# --------------------------------------------------------
# PENDING VENDORS VIEW
# Shows all vendors waiting for approval
# --------------------------------------------------------
@login_required
@role_required('vendor_officer', 'senior_management')
def vendor_pending(request):
    vendors = Vendor.objects.filter(status='pending').order_by('date_registered')
    context = {
        'vendors': vendors,
        'filter_label': 'Pending Approval',
        'pending_count': vendors.count(),
    }
    return render(request, 'vendors/vendor_pending.html', context)


# --------------------------------------------------------
# APPROVE VENDOR
# --------------------------------------------------------
@login_required
@role_required('vendor_officer', 'senior_management')
def vendor_approve(request, pk):
    vendor = get_object_or_404(Vendor, pk=pk)
    vendor.status = 'approved'
    vendor.save()
    messages.success(request, f'{vendor.company_name} has been approved!')
    return redirect('vendor-pending')


# --------------------------------------------------------
# REJECT VENDOR
# --------------------------------------------------------
@login_required
@role_required('vendor_officer', 'senior_management')
def vendor_reject(request, pk):
    vendor = get_object_or_404(Vendor, pk=pk)
    vendor.status = 'suspended'
    vendor.save()
    messages.success(request, f'{vendor.company_name} has been rejected.')
    return redirect('vendor-pending')