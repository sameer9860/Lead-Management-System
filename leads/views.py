# Updated views.py - Add these to your existing views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from django.db.models import Count,Q
from .models import Lead, LeadNote, ActivityLog
from .forms import LeadNoteForm, LeadForm
from .filters import LeadFilter
import json
from django.urls import reverse
from .forms import SetPasswordForm
from django.contrib.auth import update_session_auth_hash
# Your existing views (keep these as they are, just add activity logging)


@login_required
def dashboard(request):
    leads = Lead.objects.all()
    lead_filter = LeadFilter(request.GET, queryset=leads)
    filtered_leads = lead_filter.qs

    # Stats by status
    stats = filtered_leads.aggregate(
        total=Count('id'),
        new=Count('id', filter=Q(status='new')),
        in_progress=Count('id', filter=Q(status='in_progress')),
        converted=Count('id', filter=Q(status='converted')),
        lost=Count('id', filter=Q(status='lost'))
    )

    # Conversion rate
    conversion_rate = round((stats['converted'] / stats['total']) * 100, 2) if stats['total'] else 0

    # Source breakdown
    source_counts = filtered_leads.values('source').annotate(count=Count('id'))
    source_labels = [item['source'] for item in source_counts]
    source_data = [item['count'] for item in source_counts]

    # Log access
    ActivityLog.objects.create(user=request.user, action="Accessed dashboard")

    return render(request, "leads/dashboard.html", {
        "filter": lead_filter,
        "stats": stats,
        "conversion_rate": conversion_rate,
        "source_labels": source_labels,
        "source_data": source_data,
    })
    
    
@login_required
def reports(request):
    leads = Lead.objects.all()
    lead_filter = LeadFilter(request.GET, queryset=leads)
    filtered_leads = lead_filter.qs

    # Stats by status
    stats = filtered_leads.aggregate(
        total=Count('id'),
        new=Count('id', filter=Q(status='new')),
        in_progress=Count('id', filter=Q(status='in_progress')),
        converted=Count('id', filter=Q(status='converted')),
        lost=Count('id', filter=Q(status='lost'))
    )

    # Conversion rate
    conversion_rate = round((stats['converted'] / stats['total']) * 100, 2) if stats['total'] else 0

    # Source breakdown
    source_counts = filtered_leads.values('source').annotate(count=Count('id'))
    source_labels = [item['source'] for item in source_counts]
    source_data = [item['count'] for item in source_counts]

    # Log access
    ActivityLog.objects.create(user=request.user, action="Accessed reports")

    return render(request, "leads/reports.html", {
        "filter": lead_filter,
        "stats": stats,
        "conversion_rate": conversion_rate,
        "source_labels": source_labels,
        "source_data": source_data,
    })


@login_required
def lead_list(request):
    leads = Lead.objects.all()
    lead_filter = LeadFilter(request.GET, queryset=leads)
    
    # Log lead list access
    ActivityLog.objects.create(
        user=request.user,
        action="Viewed lead lists"
    )
    
    return render(request, "leads/list.html", {"filter": lead_filter})

@login_required
def lead_details(request, pk):
    """Updated lead details view with both traditional form and AJAX support"""
    lead = get_object_or_404(Lead, pk=pk)
    notes = lead.notes.all().order_by('-created_at')
    
    # Log view activity
    ActivityLog.objects.create(
        user=request.user,
        action=f"Viewed lead details for {lead.name}",
        lead=lead
    )
    
    
    if request.method == "POST":
        note_form = LeadNoteForm(request.POST)
        if note_form.is_valid():
            note = note_form.save(commit=False)
            note.lead = lead
            note.user = request.user
            note.save()
            
            # Log note addition
            ActivityLog.objects.create(
                user=request.user,
                action=f"Added note to lead {lead.name}",
                lead=lead
            )
            
            messages.success(request, "Note added successfully!")
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
        form = LeadForm(request.POST, user=request.user)  # pass user
        if form.is_valid():
            lead = form.save()

            # Log lead creation
            ActivityLog.objects.create(
                user=request.user,
                action=f"Created lead {lead.name} with status {lead.status.capitalize()}",
                lead=lead
            )

            messages.success(request, f"Lead {lead.name} created successfully!")
            return redirect("leads:lead_list")
    else:
        form = LeadForm(user=request.user)  # pass user

    return render(request, "leads/form.html", {"form": form, "title": "Create Lead"})

@login_required
def lead_delete(request, pk):
    lead = get_object_or_404(Lead, pk=pk)
    
    if request.method == "POST":
        lead_name = lead.name
        
        # Log deletion before actually deleting
        ActivityLog.objects.create(
            user=request.user,
            lead=lead,
            action=f"Deleted lead {lead_name}"
            
        )
        
        lead.delete()
        return redirect('leads:lead_list')
    
    return render(request, 'leads/lead_delete_confirm.html', {'lead': lead})




@login_required
def lead_update_view(request, pk):
    """Render the form page for editing a lead."""
    lead = get_object_or_404(Lead, pk=pk)
    form = LeadForm(instance=lead)
    return render(request, "leads/lead_update.html", {"form": form, "lead": lead, "title": "Update Lead"})


@login_required
def lead_update_ajax(request, pk):
    if request.method == "POST" and request.headers.get("x-requested-with") == "XMLHttpRequest":
        lead = get_object_or_404(Lead, pk=pk)
        form = LeadForm(request.POST, instance=lead)
        if form.is_valid():
            updated_lead = form.save()
            ActivityLog.objects.create(
                user=request.user,
                lead=updated_lead,
                action=f"Updated lead {updated_lead.name} with status {updated_lead.status.capitalize()}"
            )
            # send redirect URL in JSON
            return JsonResponse({
                "success": True,
                "redirect_url": reverse("leads:lead_list")
            })
        else:
            return JsonResponse({"success": False, "errors": form.errors}, status=400)

    return JsonResponse({"success": False, "message": "Invalid request"}, status=400)

# NEW AJAX Views - Add these to your existing views.py

@login_required
@require_http_methods(["POST"])
def add_note_ajax(request, lead_id):
    """AJAX endpoint to add a note to a lead"""
    try:
        lead = get_object_or_404(Lead, id=lead_id)
        
        # Get note content from POST data
        data = json.loads(request.body)
        note_content = data.get('note', '').strip()
        
        if not note_content:
            return JsonResponse({
                'success': False, 
                'error': 'Note content cannot be empty'
            })
        
        # Create the note
        note = LeadNote.objects.create(
            lead=lead,
            user=request.user,
            note=note_content
        )
        
        # Log the activity
        ActivityLog.objects.create(
            user=request.user,
            action=f"Added note to lead {lead.name}",
            lead=lead
        )
        
        # Return success response with note data
        return JsonResponse({
            'success': True,
            'note': {
                'id': note.id,
                'content': note.note,
                'user': note.user.username,
                'created_at': note.created_at.strftime('%b %d, %Y %H:%M'),
                'user_full_name': f"{note.user.first_name} {note.user.last_name}".strip() or note.user.username
            }
        })
        
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'error': 'Invalid JSON data'
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        })

@login_required
@require_http_methods(["DELETE"])
def delete_note_ajax(request, note_id):
    """AJAX endpoint to delete a note - FIXED VERSION"""
    try:
        note = get_object_or_404(LeadNote, id=note_id)
        lead = note.lead
        
        # Fixed permission check - check for user role attribute properly
        can_delete = False
        
        # Check if user is the creator of the note
        if note.user == request.user:
            can_delete = True
        
        # Check if user is superuser
        elif request.user.is_superuser:
            can_delete = True
            
        # Check if user is staff
        elif request.user.is_staff:
            can_delete = True
            
        # Check for custom role field (adjust based on your User model)
        elif hasattr(request.user, 'role') and request.user.role == 'admin':
            can_delete = True
        
        if not can_delete:
            return JsonResponse({
                'success': False, 
                'error': 'You do not have permission to delete this note'
            }, status=403)
        
        # Log the activity before deletion
        ActivityLog.objects.create(
            user=request.user,
            action=f"Deleted note from lead {lead.name}",
            lead=lead
        )
        
        note.delete()
        
        return JsonResponse({'success': True})
        
    except LeadNote.DoesNotExist:
        return JsonResponse({
            'success': False,
            'error': 'Note not found'
        }, status=404)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': f'Server error: {str(e)}'
        }, status=500)


@login_required
def get_notes_ajax(request, lead_id):
    """AJAX endpoint to fetch all notes for a lead"""
    try:
        lead = get_object_or_404(Lead, id=lead_id)
        notes = lead.notes.all().order_by('-created_at')
        
        notes_data = []
        for note in notes:
            notes_data.append({
                'id': note.id,
                'content': note.note,
                'user': note.user.username,
                'user_full_name': f"{note.user.first_name} {note.user.last_name}".strip() or note.user.username,
                'created_at': note.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                'can_delete': note.user == request.user or request.user.is_staff
            })
        
        return JsonResponse({
            'success': True,
            'notes': notes_data
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        })
        
        
        
@login_required
def note_delete_confirm(request, note_id):
    """Display confirmation page before deleting a note"""
    note = get_object_or_404(LeadNote, id=note_id)
    lead = note.lead
    
    # Check if user can delete this note
    can_delete = (
        note.user == request.user or 
        request.user.is_superuser or 
        request.user.is_staff or 
        (hasattr(request.user, 'role') and request.user.role == 'admin')
    )
    
    if not can_delete:
        messages.error(request, 'You do not have permission to delete this note.')
        return redirect('leads:lead_details', pk=lead.pk)
    
    if request.method == 'POST':
        # Log the activity before deletion
        ActivityLog.objects.create(
            user=request.user,
            action=f"Deleted note from lead {lead.name}",
            lead=lead
        )
        
        note.delete()
        messages.success(request, 'Note deleted successfully!')
        return redirect('leads:lead_details', pk=lead.pk)
    
    context = {
        'note': note,
        'lead': lead,
    }
    return render(request, 'leads/delete_confirm_notes.html', context)



@login_required
def change_password(request):
    if request.method == "POST":
        form = SetPasswordForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # keep user logged in after password change
            # messages.success(request, "Your password was changed successfully!")
            return redirect("leads:dashboard")  # change "dashboard" to your dashboard URL name
    else:
        form = SetPasswordForm(request.user)

    return render(request, "leads/change_password.html", {"form": form})

        # leads/views.py

def activity_logs(request):
    logs = ActivityLog.objects.select_related("user", "lead").order_by("-timestamp")
    return render(request, "leads/activity_logs.html", {"logs": logs})


def lead_detail(request, pk):
    lead = get_object_or_404(Lead, pk=pk)
    logs = ActivityLog.objects.filter(lead=lead).select_related("user").order_by("-timestamp")
    return render(request, "leads/lead_detail.html", {"lead": lead, "logs": logs})
