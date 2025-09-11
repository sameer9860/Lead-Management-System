# Updated urls.py - Add these to your existing urlpatterns
from django.urls import path
from . import views

app_name = "leads"

urlpatterns = [
    # Your existing URLs
    path('', views.dashboard, name='dashboard'),
    path("lead_list/", views.lead_list, name="lead_list"),
    path("lead_details/<int:pk>/", views.lead_details, name="lead_details"),
    path("form/", views.form, name="form"),
    path("lead_delete/<int:pk>/", views.lead_delete, name='lead_delete'),
     path("<int:pk>/update/", views.lead_update_view, name="lead_update_view"),
    path("<int:pk>/update-ajax/", views.lead_update_ajax, name="lead_update_ajax"),
    path("reports/", views.reports, name='reports'),
    path("change-password/", views.change_password, name="change_password"),
    
    # New AJAX endpoints
    path('ajax/lead/<int:lead_id>/add-note/', views.add_note_ajax, name='add_note_ajax'),
    path('ajax/note/<int:note_id>/delete/', views.delete_note_ajax, name='delete_note_ajax'),
    path('ajax/lead/<int:lead_id>/notes/', views.get_notes_ajax, name='get_notes_ajax'),
    
    
    path('note/<int:note_id>/delete/', views.note_delete_confirm, name='note_delete_confirm'),

    
    
    path("logs/", views.activity_logs, name="activity_logs"),   # global logs page
    
    
    path("<int:pk>/", views.lead_detail, name="lead_detail"),   # lead detail + logs
]