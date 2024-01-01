from django.shortcuts import render, redirect
from .decorators import admin_only
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from accounts.models import Profile
from events.models import Registration, Event

from django.contrib import messages

# ================================================= HOME DASHBOARD ===============================================

@admin_only
@login_required(login_url='login')
def president(request):
    profile = Profile.objects.get(id=request.user.id)
    registrations = Registration.objects.all()
    total_approved_registrations = Registration.objects.filter(approved_by_head=True).count()
    total_unapproved_registrations = Registration.objects.filter(approved_by_head=False).count()
    
    total_money = Registration.objects.filter(approved_by_head=True)
    total_money = total_money.aggregate(Sum('event__ticket_price'))["event__ticket_price__sum"]
    
    parameters = {
        'profile': profile,
        'registrations': registrations,
        'total_approved_registrations': total_approved_registrations,
        'total_unapproved_registrations': total_unapproved_registrations,
        'total_money': total_money,
    }

    return render(request, 'council/president/index.html', parameters)

# ================================================== MY COUNCIL ==================================================

@admin_only
@login_required(login_url='login')
def my_council(request):
    profile = Profile.objects.get(id=request.user.id)
    council = Profile.objects.all()
    
    parameters = {
        'profile': profile,
        'council': council,
    }
    
    return render(request, 'council/president/my_council.html', parameters)

# ================================================== MY PROFILE ==================================================

@admin_only
@login_required(login_url='login')
def president_my_profile(request):
    profile = Profile.objects.get(id=request.user.id)
    
    if request.method == "POST":
        profile_pic = request.FILES["profile_pic"]
        profile.profile_pic = profile_pic
        
        profile.save()
        
        messages.success(request, "Profile Picture has been updated successfully!")
        
        return redirect("president_my_profile")
    
    parameters = {
        'profile': profile,
    }
    
    return render(request, 'council/president/my_profile.html', parameters)

# ================================================== UPDATE PROFILE ==============================================

@admin_only
@login_required(login_url='login')
def president_update_profile(request):
    profile = Profile.objects.get(id=request.user.id)
    
    if request.method == 'POST':
        profile.first_name = request.POST['first_name']
        profile.last_name = request.POST['last_name']
        profile.email = request.POST['email']
        profile.mobile_number = request.POST['mobile_number'].replace("+91", "")
        profile.save()
        
        messages.success(request, 'Profile updated successfully!')
        
        return redirect('president_my_profile')
    
    parameters = {
        'profile': profile,
    }
    
    return render(request, 'council/president/update_profile.html', parameters)

# ================================================== EVENTS ======================================================

@admin_only
@login_required(login_url='login')
def president_events(request):
    profile = Profile.objects.get(id=request.user.id)
    events = Event.objects.all()
    
    parameters = {
        'profile': profile,
        'events': events,
    }
    
    return render(request, 'council/president/events.html', parameters)

# ========================================== PARTICULAR EVENT DETAILS ============================================

@admin_only
@login_required(login_url='login')
def event_details(request, slug):
    profile = Profile.objects.get(id=request.user.id)
    event = Event.objects.get(slug=slug)
    registrations = Registration.objects.filter(event=event)
    approved_registrations = Registration.objects.filter(event=event, approved_by_head=True).count()
    unapproved_registrations = Registration.objects.filter(event=event, approved_by_head=False).count()
    
    total_money = Registration.objects.filter(event=event, approved_by_head=True)
    total_money = total_money.aggregate(Sum('event__ticket_price'))["event__ticket_price__sum"]
    
    
    parameters = {
        'profile': profile,
        'event': event,
        'registrations': registrations,
        'approved_registrations': approved_registrations,
        'unapproved_registrations': unapproved_registrations,
        'total_money': total_money
    }
    
    return render(request, 'council/president/event_details.html', parameters)