from django.urls import path
from . import views

app_name = "leads"

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path("lead_list/", views.lead_list, name="lead_list"),
    path("lead_details/<int:pk>/", views.lead_details, name="lead_details"), 
    path("form/", views.form, name="form"),
    path("lead_delete/<int:pk>", views.lead_delete, name='lead_delete'),
]
