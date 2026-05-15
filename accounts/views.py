from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import CustomUser


def register_view(request):
    if request.method == 'POST':
        username  = request.POST.get('username')
        email     = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        role      = request.POST.get('role')
        company   = request.POST.get('company_name')
        phone     = request.POST.get('phone_number')

        if password1 != password2:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'accounts/register.html')

        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken.')
            return render(request, 'accounts/register.html')

        CustomUser.objects.create_user(
            username=username,
            email=email,
            password=password1,
            role=role,
            company_name=company,
            phone_number=phone,
        )
        messages.success(request, 'Account created! Please log in.')
        return redirect('login')

    return render(request, 'accounts/register.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')

            if user.role == CustomUser.VENDOR_OFFICER:
                return redirect('directory-search')
            elif user.role == CustomUser.COMPLIANCE_OFFICER:
                return redirect('compliance-dashboard')
            elif user.role == CustomUser.SENIOR_MANAGEMENT:
                return redirect('dashboard-home')
            elif user.role == CustomUser.VENDOR:
                return redirect('vendor-profile')
            else:
                return redirect('dashboard-home')
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'accounts/login.html')


def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('login')


@login_required
def vendor_profile(request):
    from vendors.models import Vendor

    # Get or check if vendor has a profile
    try:
        vendor = request.user.vendor_profile
    except:
        vendor = None

    if request.method == 'POST':
        certificate_name   = request.POST.get('certificate_name')
        certificate_expiry = request.POST.get('certificate_expiry')
        certificate_file   = request.FILES.get('certificate_file')

        if vendor:
            # Update existing vendor profile certificates
            if certificate_name:
                vendor.certificate_name = certificate_name
            if certificate_expiry:
                vendor.certificate_expiry = certificate_expiry
            if certificate_file:
                vendor.certificate_file = certificate_file
            vendor.save()
            messages.success(request, 'Certificate updated successfully!')
            return redirect('vendor-profile')

        else:
            # Create new vendor profile
            company_name        = request.POST.get('company_name')
            registration_number = request.POST.get('registration_number')
            email               = request.POST.get('email')
            phone               = request.POST.get('phone')
            address             = request.POST.get('address')
            services_offered    = request.POST.get('services_offered')

            # Validate required fields
            if not registration_number:
                messages.error(request, 'Registration number is required.')
                return render(request, 'accounts/vendor_profile.html', {'vendor': None})

            if not services_offered:
                messages.error(request, 'Please describe your services.')
                return render(request, 'accounts/vendor_profile.html', {'vendor': None})

            # Check if registration number already exists
            if Vendor.objects.filter(registration_number=registration_number).exists():
                messages.error(request, f'Registration number "{registration_number}" is already taken. Please use a different one.')
                return render(request, 'accounts/vendor_profile.html', {'vendor': None})

            # Check if email already exists
            if Vendor.objects.filter(email=email).exists():
                messages.error(request, f'Email "{email}" is already registered to another vendor.')
                return render(request, 'accounts/vendor_profile.html', {'vendor': None})

            # All good — create the vendor profile
            Vendor.objects.create(
                user=request.user,
                company_name=company_name or request.user.company_name,
                registration_number=registration_number,
                email=email or request.user.email,
                phone=phone or request.user.phone_number,
                address=address,
                services_offered=services_offered,
                certificate_name=certificate_name,
                certificate_expiry=certificate_expiry,
                certificate_file=certificate_file,
                status='pending',
            )
            messages.success(request, 'Vendor profile created successfully! Awaiting approval.')
            return redirect('vendor-profile')

    context = {
        'vendor': vendor,
    }
    return render(request, 'accounts/vendor_profile.html', context)