from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomUserCreationForm , CustomUserUpdateForm
from django.contrib.auth import  login, logout
from django.contrib.auth import views as auth_views
from django.http import JsonResponse
from leads.models import ActivityLog
from django.urls import reverse
from .utils import is_email_valid, forget_password_email as forget_password_email
from .models import OTP, CustomUser
from django.contrib.auth.password_validation import validate_password


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


def forget_password(request):
    if request.method == "POST":
        email = request.POST.get("email")
        if not is_email_valid(email):
            messages.error(request, "Enter a valid email")
            return redirect("accounts:forget_password")

        try:
            forget_password_email(email)
        except Exception as e:
            messages.error(request, str(e))
            return redirect("accounts:forget_password")

        print(email, "Email sent successfully")
        messages.success(request, "Email sent successfully. Please check your inbox")
        return redirect("accounts:otp_confirmation")

    return render(request, "accounts/forget_password.html")


def otp_confirmation(request):
    if request.method == "POST":
        otp = request.POST.get("otp")
        user_id = OTP.check_otp(otp)
        if user_id is None:
            messages.error(request, "Invalid OTP, please try again")
            return redirect("accounts:otp_confirmation")

        return redirect("accounts:set_new_password", user_id=user_id)

    return render(request, "accounts/otp_confirmation.html")


def set_new_password(request, user_id=None):
    if request.method == "POST":
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        if password1 != password2:
            messages.error(request, "Passwords do not match")
            return redirect("accounts:set_new_password")

        try:
            validate_password(password1)
        except Exception as e:
            for error in list(e):
                messages.error(request, str(error))
            return redirect("accounts:set_new_password")
        else:
            if user_id is not None:
                user = CustomUser.objects.filter(id=user_id).first()
                if user is None:
                    messages.error(request, "User does not exist")
                    return redirect("accounts:set_new_password")

            user.set_password(password1)
            user.save()
            messages.success(request, "Password changed successfully")
            return redirect("accounts:login")

    return render(request, "accounts/new_password.html")