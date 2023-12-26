from django.shortcuts import render, redirect
from .decorators import admin_only

from django.db.models import Sum
from accounts.models import Profile
from events.models import Registration, Event

@admin_only
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
    
