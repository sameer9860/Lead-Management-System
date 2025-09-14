from django.contrib import admin
from .models import Lead, LeadNote, ActivityLog

from django.contrib import admin
from .models import Lead

@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'status', 'assigned_to', 'created_at')
    search_fields = ('name', 'email', 'phone' , 'company')
    list_filter = ('status', 'assigned_to', 'created_at')


@admin.register(LeadNote)
class LeadNoteAdmin(admin.ModelAdmin):
    list_display = ("lead", "user", "created_at")
    search_fields = ("lead__name", "user__username", "note")

@admin.register(ActivityLog)
class ActivityLogAdmin(admin.ModelAdmin):
    list_display = ("user", "action", "lead", "timestamp")
    search_fields = ("user__username", "action", "lead__name")
