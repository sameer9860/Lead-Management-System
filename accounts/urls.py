# accounts/urls.py
from django.urls import path
from django.contrib.auth import views as auth_views
from .views import LoginView, register
from . import views

app_name = "accounts"

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('register/', views.register, name='register'), 
    path("logout/", views.logout_view, name="logout_view"),
    path('profile/', views.profile, name='profile'),
]

