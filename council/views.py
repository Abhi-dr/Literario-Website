from django.shortcuts import render, redirect
from .decorators import admin_only
from accounts.models import Profile
from django.contrib.auth.decorators import login_required
from events.models import Event, Registration

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

