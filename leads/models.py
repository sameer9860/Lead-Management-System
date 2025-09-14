from django.db import models
from django.conf import settings

class Lead(models.Model):
    STATUS_CHOICES = [
        ("new", "New"),
        ("in_progress", "In Progress"),
        ("converted", "Converted"),
        ("lost", "Lost"),
    ]

    name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=15, blank=True, null=True)
    company = models.CharField(max_length=200, blank=True, null=True)
    source = models.CharField(max_length=200, blank=True, null=True)  # e.g., Website, Referral
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="new")
    assigned_to = models.ForeignKey(
    settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.status})"


class LeadNote(models.Model):
    lead = models.ForeignKey(Lead, on_delete=models.CASCADE, related_name="notes")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    note = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Note by {self.user.username} on {self.lead.name}"


class ActivityLog(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    lead = models.ForeignKey("Lead", on_delete=models.SET_NULL, null=True, blank=True)
    action = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.action} ({self.timestamp:%Y-%m-%d %H:%M})"

