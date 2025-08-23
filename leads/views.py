from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from .models import Lead
from .forms import LeadNoteForm,LeadForm
from django.contrib import messages
from django.db.models import Count
from .filters import LeadFilter

# Create your views here.
@login_required
def dashboard(request):
    leads = Lead.objects.all()

    # Apply filter
    lead_filter = LeadFilter(request.GET, queryset=leads)
    filtered_leads = lead_filter.qs

    # Stats by your statuses
    stats = {
        "total": filtered_leads.count(),
        "new": filtered_leads.filter(status="New").count(),
        "in_progress": filtered_leads.filter(status__icontains="progress").count(),
        "converted": filtered_leads.filter(status="Converted").count(),
        "lost": filtered_leads.filter(status="Lost").count(),
    }

    return render(request, "leads/dashboard.html", {
        "filter": lead_filter,
        "stats": stats,
    })



@login_required
def lead_list(request):
    leads = Lead.objects.all()
    lead_filter = LeadFilter(request.GET, queryset=leads)
    return render(request, "leads/list.html", {"filter": lead_filter})


@login_required
def lead_details(request, pk):
    lead = get_object_or_404(Lead, pk=pk)
    notes = lead.notes.all()
    
    if request.method == "POST":
        note_form = LeadNoteForm(request.POST)
        if note_form.is_valid():
            note = note_form.save(commit=False)
            note.lead = lead
            note.user = request.user
            note.save()
            return redirect("leads:lead_details", pk=lead.pk)
    else:
        note_form = LeadNoteForm()

    context = {
        "lead": lead,
        "notes": notes,
        "note_form": note_form,
        
    }
    return render(request, "leads/lead_details.html", context)


@login_required
def form(request):
    if request.method == "POST":
        form = LeadForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("leads:lead_list")
    else:
        form = LeadForm()
    return render(request, "leads/form.html", {"form": form, "title": "Create Lead"})



def lead_delete(request, pk):
    if request.method  == "POST":
       lead = get_object_or_404(Lead, pk=pk)
       if request.method == 'POST':
         lead.delete()
         return redirect('leads:lead_list' , pk = lead.pk)
    return render(request, 'leads/lead_details.html', {'lead': lead})
