# accounts/urls.py
from django.urls import path
from django.contrib.auth import views as auth_views
from .views import LoginView
from . import views

app_name = "accounts"

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('register/', views.register, name='register'), 
    path("logout/", views.logout_view, name="logout_view"),
    path('profile/', views.profile, name='profile'),
    path("profile/update/", views.update_profile, name="update_profile"),
 # forgot password
    path("forget_password/", views.forget_password, name="forget_password"),
    path("otp_confirmation/", views.otp_confirmation, name="otp_confirmation"),
    path(
        "set_new_password/<int:user_id>/",
        views.set_new_password,
        name="set_new_password",
    ),

]

    