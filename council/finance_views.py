from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .decorators import finance_head_only
from events.models import Event, Registration
from accounts.models import Profile
from django.core.mail import send_mail

from django.contrib import messages

@login_required(login_url='login')
@finance_head_only
def approve_registrations(request):
    profile = Profile.objects.get(id=request.user.id)
    registrations = Registration.objects.filter(approved_by_head=False)
    
    parameters = {
        'profile': profile,
        'registrations': registrations
    }
    
    return render(request, 'council/finance/approve_registrations.html', parameters)

@login_required(login_url='login')
@finance_head_only
def approve_registration(request, registration_id):    
    registration = Registration.objects.get(id=registration_id)
    registration.approved_by_head = True
    registration.save()
    
    # Sending Mail
        
    myfile = open(r"council\confirmed.txt")

    email_subject = ' Confirmation To The Talk Show ❤️ '
    email_body = eval(myfile.read())
    email_from = 'Divyanshu Khandelwal'
    email_to = [registration.email]

    # Send the email
    send_mail(email_subject, email_body, email_from, email_to)
    
    messages.success(request, "Registration approved successfully!")
    return redirect('approve_registrations')

@login_required(login_url='login')
@finance_head_only
def reject_registration(request, registration_id):
    registration = Registration.objects.get(id=registration_id)
    registration.delete()
    
    messages.error(request, "Registration rejected successfully!")
    return redirect('approve_registrations')