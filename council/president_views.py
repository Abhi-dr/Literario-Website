from django.shortcuts import render, redirect
from .decorators import admin_only

from accounts.models import Profile
from events.models import Registration, Event

@admin_only
def president(request):
    profile = Profile.objects.get(id=request.user.id)
    registrations = Registration.objects.all()
    total_approved_registrations = Registration.objects.filter(approved_by_head=True).count()
    total_unapproved_registrations = Registration.objects.filter(approved_by_head=False).count()
    
    parameters = {
        'profile': profile,
        'registrations': registrations,
        'total_approved_registrations': total_approved_registrations,
        'total_unapproved_registrations': total_unapproved_registrations
    }

    return render(request, 'council/president/index.html', parameters)
    
