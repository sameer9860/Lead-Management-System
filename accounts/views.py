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

    def form_valid(self, form):
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Login failed. Please check your username and password.")
        return super().form_invalid(form)
    
    
    
    # if request.method == "POST":
    #     username = request.POST.get("username")
    #     password = request.POST.get("password")

    #     user = authenticate(request, username=username, password=password)

    #     if user is not None:
    #         login(request, user)
    #         return redirect("app:dashboard")

    #     messages.error(request, "Invalid username or password")
    #     return redirect("accounts:school_admin_login")

    # form = SchoolAdminLoginForm()

    # context = {"form": form}
    # return render(request, "accounts/login.html", context)
@login_required
def register(request):
    
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "User registered successfully")
            
            return redirect("leads:dashboard")
        else:
            messages.error(request, "Registration failed. Please correct the errors below.")
            
            return render(request, "accounts/register.html", {"form": form})
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


    
 