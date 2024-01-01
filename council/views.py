from django.shortcuts import render, redirect
from .decorators import admin_only
from accounts.models import Profile
from django.contrib.auth.decorators import login_required
from events.models import Event, Registration
from django.core.mail import send_mail

from django.contrib import messages


def index(request):
    user = request.user
    
    if user.is_superuser:
        return redirect('president')

    return redirect('member')

# ===============================================================================================================
# ================================================ MEMBERS ======================================================
# ===============================================================================================================

@login_required(login_url='login')
def member(request):
    profile = Profile.objects.get(id=request.user.id)
    referrals = Registration.objects.filter(referral_code = profile.referral_code)  
    
    parameters = {
        'profile': profile,
        'referrals': referrals
    }
    
    if profile.username == "finance_head":
        total_approved_registrations = Registration.objects.filter(approved_by_head=True).count()
        parameters['total_approved_registrations'] = total_approved_registrations
    
    return render(request, 'council/member/index.html', parameters)

# ================================================= MY PROFILE ==================================================

@login_required(login_url='login')
def my_profile(request):
    profile = Profile.objects.get(id=request.user.id)
    
    if request.method == "POST":
        
        if request.FILES.get("profile_pic", False):
        
            profile_pic = request.FILES["profile_pic"]
            profile.profile_pic = profile_pic
        
            profile.save()
        
        messages.success(request, "Profile Picture has been updated successfully!")
        
        return redirect("my_profile")
    
    parameters = {
        'profile': profile,
    }
    
    return render(request, 'council/member/my_profile.html', parameters)

# ================================================= UPDATE PROFILE ==============================================

@login_required(login_url='login')
def update_profile(request):
    profile = Profile.objects.get(id=request.user.id)
    
    if request.method == 'POST':
        profile.first_name = request.POST['first_name']
        profile.last_name = request.POST['last_name']
        profile.email = request.POST['email']
        profile.mobile_number = request.POST['mobile_number'].replace("+91", "")
        profile.qr_code = request.FILES.get('qr_code')
        profile.save()
        
        messages.success(request, 'Profile updated successfully!')
        
        return redirect('my_profile')
    
    parameters = {
        'profile': profile,
    }
    
    return render(request, 'council/member/update_profile.html', parameters)

# ================================================= CHANGE PASSWORD =============================================

@login_required(login_url='login')
def change_password(request):
    profile = Profile.objects.get(id=request.user.id)
    
    if request.method == 'POST':
        current_password = request.POST['current_password']
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']
        
        if profile.check_password(current_password):
            if new_password == confirm_password:
                profile.set_password(new_password)
                profile.save()
                
                messages.success(request, 'Password changed successfully! Login Again!')
                
                return redirect('my_profile')
            else:
                messages.error(request, 'New password and confirm password do not match!')
                return redirect('change_password')
        else:
            messages.error(request, 'Current password is incorrect!')
            return redirect('change_password')
    
    parameters = {
        'profile': profile,
    }
    
    return render(request, 'council/member/change_password.html', parameters)

# ================================================= MY REGISTRATIONS ============================================

@login_required(login_url='login')
def my_registrations(request, slug):
    profile = Profile.objects.get(id=request.user.id)
    event = Event.objects.get(slug=slug)
    
    if request.method == 'POST':
        name = request.POST.get('name')
        course = request.POST.get('course')
        year = request.POST.get('year')
        email = request.POST.get('email')
        day_host = request.POST.get('day_host')
        registration_type = request.POST.get('registration_type')
        mode_of_payment = request.POST.get('mode_of_payment')
        
        if Registration.objects.filter(email=email).exists():
            messages.error(request, "You have already registered for this event.")
            return redirect('my_registrations', slug=slug)
    
        new_registration = Registration(
            name = name,
            course = course,
            year = year,
            email = email,
            event = event,
            hosteller_dayScholar = day_host,
            referral_name = profile,
            referral_code = profile.referral_code,
            approved_by_head = True,
            mode_of_payment = mode_of_payment
        )
        
        if registration_type == "Group":
            new_registration.registration_type = "Group"
        elif registration_type == "Duo":
            new_registration.registration_type = "Duo"
        else:
            new_registration.registration_type = "Solo"
            
        new_registration.save()
        
        event.total_tickets = event.total_tickets - 1
        event.save()
        
        myfile = f"""Tickets Confirmed! Club Literario!

Dear {name},

CONGRATULATIONS! 🎉 Your Ticket for our magnificent event – “{ event.name }” has been confirmed. We will be excitedly waiting for you to be a keen audience.🙌

Stand by your mail for further updates!

For any kind of doubts or burning queries, we always welcome you;
Mr. Divyanshu Khandelwal: 8273619318
Mr. Priyanshu Gera: 7302068234

Hope you have a great day.🌸

Best wishes,
Divyanshu Khandelwal,
Technical Team,
Club Literario
GLA University Mathura."""

        email_subject = ' Confirmation To The Talk Show ❤️ '
        email_body = myfile
        email_from = 'Club Literario'
        email_to = [email]

        # Send the email
        send_mail(email_subject, email_body, email_from, email_to)

                
        new_registration.save()
        
        messages.success(request, "Welcome to the most awaited event of the year! We are glad to have you on board!".title())

        
        return redirect('my_registrations', slug=slug)
    
    parameters = {
        'profile': profile,
        'event': event
    }
    
    return render(request, 'council/member/my_registrations.html', parameters)

# ================================================= EVENT CHOICE ================================================

@login_required(login_url='login')
def event_choice(request):
    profile = Profile.objects.get(id=request.user.id)
    events = Event.objects.all()
    
    parameters = {
        'profile': profile,
        'events': events
    }
    
    return render(request, 'council/member/event_choice.html', parameters)