from django import forms
from .models import Lead, LeadNote
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import SetPasswordForm


User = get_user_model()

class LeadForm(forms.ModelForm):
    class Meta:
        model = Lead
        fields = ["name", "email", "phone", "company", "source", "status", "assigned_to"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "phone": forms.TextInput(attrs={"class": "form-control"}),
            "company": forms.TextInput(attrs={"class": "form-control"}),
            "source": forms.TextInput(attrs={"class": "form-control"}),
            "status": forms.Select(attrs={"class": "form-control"}),
            "assigned_to": forms.Select(attrs={"class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)  # take logged-in user from view
        super().__init__(*args, **kwargs)

        if user:
            if user.role == "admin":
                # Admin can assign to anyone
                self.fields["assigned_to"].queryset = User.objects.all()
            elif user.role == "sales_manager":
                # Sales Manager → only Sales Executives
                self.fields["assigned_to"].queryset = User.objects.filter(role="sales_executive")
            else:
                # Sales Executive → cannot assign, so hide field
                self.fields.pop("assigned_to", None)
                
                
                

class LeadNoteForm(forms.ModelForm):
    class Meta:
        model = LeadNote
        fields = ["note"]
        widgets = {
            "note": forms.Textarea(attrs={"class": "form-control", "rows": 3})
        }
        
        
