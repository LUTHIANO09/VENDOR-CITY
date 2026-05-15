from django.urls import path
from . import views

# URL patterns for the vendors app
# name= parameter allows us to reference URLs in templates using {% url %}
urlpatterns = [
    path('', views.vendor_list, name='vendor-list'),
    path('<int:pk>/', views.vendor_detail, name='vendor-detail'),
    path('approved/', views.vendor_approved, name='vendor-approved'),
    path('expired/', views.vendor_expired, name='vendor-expired'),
    path('pending/', views.vendor_pending, name='vendor-pending'),
    path('<int:pk>/approve/', views.vendor_approve, name='vendor-approve'),
    path('<int:pk>/reject/', views.vendor_reject, name='vendor-reject'),

]