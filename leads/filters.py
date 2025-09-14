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

    # --- Date Range Filters ---
    start_date = django_filters.DateFilter(
        field_name="created_at",
        lookup_expr="gte",
        label="Start Date",
        widget=forms.DateInput(attrs={"type": "date", "class": "form-control"})
    )
    
    end_date = django_filters.DateFilter(
        field_name="created_at",
        lookup_expr="lte",
        label="End Date",
        widget=forms.DateInput(attrs={"type": "date", "class": "form-control"})
    )

    class Meta:
        model = Lead
        fields = ["name", "email", "status", "start_date", "end_date"]
