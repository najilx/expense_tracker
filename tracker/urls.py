from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import *
from tracker import views as tracker_views

urlpatterns = [
    path('', tracker_views.home_redirect, name='home'),
    path('register/', views.register, name='register'),
    path('login/',auth_views.LoginView.as_view(template_name='tracker/login.html'), name='login'),
    path('logout/',auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('dashboard/', dashboard, name='dashboard'),
    path('add/', add_transaction, name='add_transaction'),
    path('edit/<int:pk>/', update_transaction, name='update_transaction'),
    path('delete/<int:pk>/', delete_transaction, name='delete_transaction'),
]