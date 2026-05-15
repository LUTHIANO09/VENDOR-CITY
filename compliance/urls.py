from django.urls import path
from . import views

urlpatterns = [
    path('', views.compliance_dashboard, name='compliance-dashboard'),
    path('vendor/<int:pk>/', views.compliance_vendor_detail, name='compliance-vendor-detail'),
]