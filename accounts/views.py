from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomUserCreationForm , CustomUserUpdateForm
from django.contrib.auth import  login, logout
from django.contrib.auth import views as auth_views
from django.http import JsonResponse
from leads.models import ActivityLog
from django.urls import reverse


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




def is_ajax(request):
    return request.headers.get("x-requested-with") == "XMLHttpRequest"

class LoginView(auth_views.LoginView):
    template_name = "accounts/login.html"
    redirect_authenticated_user = True

    def form_valid(self, form):
        login(self.request, form.get_user())

        # Log login
        ActivityLog.objects.create(user=self.request.user, action="Logged in")

        if is_ajax(self.request):
            return JsonResponse({"success": True, "redirect_url": self.get_success_url()})
        return super().form_valid(form)

    def form_invalid(self, form):
        if is_ajax(self.request):
            return JsonResponse({"success": False, "errors": form.errors})
        messages.error(self.request, "Login failed. Please check your username and password.")
        return super().form_invalid(form)

@login_required
def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()

            # Log activity
            ActivityLog.objects.create(
                user=request.user,
                action=f"Registered new user: {user.username} (Role: {user.role})"
            )

            # If AJAX request, return JSON
            if is_ajax(request):
                return JsonResponse({
                    "success": True,
                    "message": f"User {user.username} registered successfully!",
                    "redirect_url": "/leads/dashboard/"  # or use reverse("leads:dashboard")
                })

            # Normal POST redirect
            return redirect("leads:dashboard")
        else:
            # AJAX error response
            if is_ajax(request):
                return JsonResponse({
                    "success": False,
                    "errors": form.errors
                }, status=400)

            # Normal POST response with messages
            messages.error(
                request, "Registration failed. Please correct the errors below."
            )
            return render(request, "accounts/register.html", {"form": form})
    else:
        form = CustomUserCreationForm()
    return render(request, "accounts/register.html", {"form": form})


@login_required
def logout_view(request):
    # Log the logout activity
    ActivityLog.objects.create(
        user=request.user,
        action=f"User logged out: {request.user.username} (Role: {request.user.role})"
    )

    # Logout the user
    logout(request)
    return redirect("accounts:login")


@login_required
def profile(request):
    # Log profile view ONLY if NOT an AJAX request
    if not request.headers.get("x-requested-with") == "XMLHttpRequest":
        ActivityLog.objects.create(
            user=request.user,
            action=f"Viewed profile: {request.user.username} (Role: {request.user.role})"
        )

    # Handle AJAX request
    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        data = {
            "username": request.user.username,
            "first_name": request.user.first_name,
            "last_name": request.user.last_name,
            "email": request.user.email,
            "phone_no": getattr(request.user, "phone_no", ""),
            "address": getattr(request.user, "address", ""),
            "role": getattr(request.user, "role", ""),
            "profile_pic": request.user.profile_pic.url if getattr(request.user, "profile_pic", None) else ""
        }
        return JsonResponse(data)

    # Normal page render
    return render(request, "accounts/profile.html", {"user": request.user})



@login_required
def update_profile(request):
    user = request.user

    if request.method == "POST":
        form = CustomUserUpdateForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            old_data = {field: getattr(user, field) for field in form.fields}  # capture old values
            form.save()

            # Log what changed
            changed_fields = []
            for field in form.fields:
                old_value = old_data[field]
                new_value = getattr(user, field)
                if old_value != new_value:
                    changed_fields.append(f"{field}: '{old_value}' → '{new_value}'")

            action_text = "Updated profile"
            if changed_fields:
                action_text += " (" + ", ".join(changed_fields) + ")"

            ActivityLog.objects.create(
                user=user,
                action=action_text
            )

            if request.headers.get("x-requested-with") == "XMLHttpRequest":
             return JsonResponse({
        "success": True,
        "message": "Profile updated successfully!",
        "redirect_url": reverse("accounts:profile")  # send URL to frontend
    })


        else:
            if request.headers.get("x-requested-with") == "XMLHttpRequest":
                return JsonResponse({"success": False, "errors": form.errors}, status=400)

    else:
        form = CustomUserUpdateForm(instance=user)

    return render(request, "accounts/update_profile.html", {"form": form})