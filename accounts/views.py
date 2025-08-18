from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomUserCreationForm
from .models import CustomUser
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import views as auth_views



class LoginView(auth_views.LoginView):
    template_name = "accounts/login.html"
    redirect_authenticated_user = True

@login_required

def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "User registered successfully")
            return redirect("leads:dashboard")
    else:
        form = CustomUserCreationForm()
    return render(request, "accounts/register.html", {"form": form})



@login_required
def logout_view(request):
    logout(request)
    return redirect("accounts:login")

@login_required
def profile(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully")
            return redirect("accounts:profile")
    else:
        form = CustomUserCreationForm(instance=request.user)
    return render(request, "accounts/profile.html", {"form": form})


    
 