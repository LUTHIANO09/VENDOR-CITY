from django.urls import path
from . import views

urlpatterns = [
    path('', views.directory_search, name='directory-search'),
]