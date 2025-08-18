# accounts/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser 

class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    email = forms.EmailField(required=True )
    phone_no = forms.CharField(required=False , max_length=10 )
    address = forms.CharField(required=False, max_length=255)
    profile_pic = forms.ImageField(required=False)
    role = forms.ChoiceField(choices=CustomUser.ROLE_CHOICES)

    class Meta:
        model = CustomUser
        fields = ["username", "email", "first_name", "last_name", "phone_no", "address", "profile_pic", "role", "password1", "password2"]
