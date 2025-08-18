from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def dashboard(request):
    """
    Render the dashboard page for leads.
    """
    
    return render(request, 'leads/dashboard.html')
