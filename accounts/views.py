from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomUserCreationForm
from .models import CustomUser
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import views as auth_views

# def login_view(request):
#     if request.user.is_authenticated:  # same as redirect_authenticated_user=True
#         return redirect("dashboard")   # adjust to your desired redirect

#     if request.method == "POST":
#         form = LoginForm(request, data=request.POST)
#         if form.is_valid():
#             user = form.get_user()
#             login(request, user)
#             return redirect("dashboard")  # or use next = request.GET.get("next")
#         else:
#             messages.error(request, "Login failed. Please check your username and password.")
#     else:
#         form = LoginForm()

#     return render(request, "accounts/login.html", {"form": form})




class LoginView(auth_views.LoginView):
    template_name = "accounts/login.html"
    redirect_authenticated_user = True

    def form_valid(self, form):
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(
            self.request, "Login failed. Please check your username and password."
        )
        return super().form_invalid(form)


@login_required
def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()

            return redirect("leads:dashboard")
        else:
            messages.error(
                request, "Registration failed. Please correct the errors below."
            )

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
        form = CustomUserCreationForm(
            request.POST, request.FILES, instance=request.user
        )
        if form.is_valid():
            form.save()
            return redirect("accounts:profile")
    else:
        form = CustomUserCreationForm(instance=request.user)
    return render(request, "accounts/profile.html", {"form": form})
