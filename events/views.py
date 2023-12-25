from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail

from .models import Event, Registration
from accounts.models import Profile

def registration(request):
    
    if request.method == "POST":
        name = request.POST.get('name')
        course = request.POST.get('course')
        year = request.POST.get('year')
        email = request.POST.get('email')
        event_id = request.POST.get('event')
        referral_code = request.POST.get('referral_code')
        
        # Check if user has already registered for this event
        if Registration.objects.filter(email=email).exists():
            messages.error(request, "You have already registered for this event.")
            return redirect('registration')
    
        new_registration = Registration(
            name = name,
            course = course,
            year = year,
            email = email,
            event = Event.objects.get(id=event_id),
            referral_name = Profile.objects.get(referral_code=referral_code),
            referral_code = referral_code
        )
        
        new_registration.save()
        
        messages.success(request, "Welcome to the most awaited event of the year! We are glad to have you on board!".title())
       
        return redirect('registration')
    
    events = Event.objects.all()
    referrals = Profile.objects.all()
    
    parameters = {
        'events': events,
        'referrals': referrals,
    }
    
    return render(request, "home/registration.html", parameters)

