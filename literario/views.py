from django.shortcuts import render, redirect
from accounts.models import Profile

from django.contrib import messages


def registerMe(request):
    
    if request.method == "POST":
        first_name = request.POST.get('first_name').strip()
        last_name = request.POST.get('last_name').strip()
        gender = request.POST.get("gender")
        mobile_number = request.POST.get('phone')
        email = request.POST.get('email')
        course = request.POST.get('course')
        year = request.POST.get('year')
        team = request.POST.get('team')
        post = request.POST.get('post')
        
        if Profile.objects.filter(username=username).exists():
            messages.error(request, "Username Already Exists!")
            return redirect('registerMe')

        new_user = Profile.objects.create(
            first_name = first_name,
            last_name = last_name,
            gender = gender,
            mobile_number = mobile_number,
            email = email,
            course = course,
            year = year,
            team = team,
            post = post,       
            is_member = True,
        )
        
        username = first_name + "_" + str(mobile_number)[-4:]
        
        new_user.username = username
        
        new_user.save()
        
        messages.success(request, "You have been registered successfully! Login Now")

        return redirect('login')
        
    
    return render(request, 'registerMe.html')


def page_not_found_view(request, exception):
    return render(request, '404.html', status=404)
