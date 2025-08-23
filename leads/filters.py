import django_filters
from django import forms
from .models import Lead

class LeadFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(
        field_name="name",
        lookup_expr="icontains",
        label="Name",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter name"})
    )

    email = django_filters.CharFilter(
        field_name="email",
        lookup_expr="icontains",
        label="Email",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter email"})
    )

    status = django_filters.ChoiceFilter(
        choices=Lead.STATUS_CHOICES,
        label="Status",
        widget=forms.Select(attrs={"class": "form-select"})
    )

    class Meta:
        model = Lead
        fields = ["name", "email", "status"]
