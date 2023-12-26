from django.shortcuts import render, redirect
from .decorators import admin_only
from accounts.models import Profile
from django.contrib.auth.decorators import login_required
from events.models import Event, Registration


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

@login_required(login_url='login')
def my_profile(request):
    profile = Profile.objects.get(id=request.user.id)
    
    parameters = {
        'profile': profile,
    }
    
    return render(request, 'council/member/my_profile.html', parameters)