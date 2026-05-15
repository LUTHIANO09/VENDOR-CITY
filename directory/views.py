from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from accounts.decorators import role_required
from vendors.models import Vendor


@login_required
@role_required('vendor_officer', 'senior_management')
def directory_search(request):
    query = request.GET.get('q', '')
    status_filter = request.GET.get('status', '')

    vendors = Vendor.objects.all()

    if query:
        vendors = vendors.filter(
            company_name__icontains=query
        ) | vendors.filter(
            services_offered__icontains=query
        ) | vendors.filter(
            certificate_name__icontains=query
        )

    if status_filter:
        vendors = vendors.filter(status=status_filter)

    context = {
        'vendors': vendors,
        'query': query,
        'status_filter': status_filter,
        'total_count': Vendor.objects.count(),
        'approved_count': Vendor.objects.filter(status='approved').count(),
        'pending_count': Vendor.objects.filter(status='pending').count(),
        'suspended_count': Vendor.objects.filter(status='suspended').count(),
    }
    return render(request, 'directory/directory_search.html', context)