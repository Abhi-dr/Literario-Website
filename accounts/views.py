from django.shortcuts import render,redirect
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.contrib import auth

def register(request):
    if request.method == 'POST':
        userEmail= request.POST.get('email')  
        password = request.POST.get('password')


        new_user = User.objects.create(
            userEmail=userEmail, 
        )
        new_user.set_password(password)
        new_user.save()
        subject = 'Welcome to literario website'
        message = 'Thank you for signing up on our Website. We are excited to have you!'
        from_email = ''  
        recipient_list = [new_user.email]

        send_mail(subject, message, from_email, recipient_list, fail_silently=False)

        return redirect('login')
    return render(request, 'accounts/register.html')
def login(request):
    if request.method=='POST':
        email=request.POST.get('email')
        p_word=request.POST.get('pwd')

        user=auth.authenticate(email=email,password=p_word)
        if user is not None:
            auth.login(request,user)
            return redirect('index')
        else:
            return redirect('login')
    return render(request,'accounts/login.html') 
