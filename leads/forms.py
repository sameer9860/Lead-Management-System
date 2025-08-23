from django import forms
from .models import Lead, LeadNote

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

class LeadNoteForm(forms.ModelForm):
    class Meta:
        model = LeadNote
        fields = ["note"]
        widgets = {
            "note": forms.Textarea(attrs={"class": "form-control", "rows": 3})
        }
        
        
