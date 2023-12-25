from django.shortcuts import render,redirect
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib import messages

# def register(request):
#     if request.method == 'POST':
#         userEmail= request.POST.get('email')  
#         password = request.POST.get('password')


#         new_user = User.objects.create(
#             userEmail=userEmail, 
#         )
#         new_user.set_password(password)
#         new_user.save()
#         subject = 'Welcome to literario website'
#         message = 'Thank you for signing up on our Website. We are excited to have you!'
#         from_email = ''  
#         recipient_list = [new_user.email]

#         send_mail(subject, message, from_email, recipient_list, fail_silently=False)

#         return redirect('login')
#     return render(request, 'accounts/register.html')


def login(request):
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')

        user=auth.authenticate(username=username,password=password)
        
        if user is not None:
            auth.login(request,user)
            return redirect('council')
        
        else:
            messages.info(request, 'Username or Password is incorrect')
            return redirect('login')        
    return render(request,'accounts/login.html') 
