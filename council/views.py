from django.shortcuts import render, redirect
from .decorators import admin_only


def index(request):
    user = request.user
    
    if user.is_superuser:
        return redirect('president')

    return redirect('member')
    

def member(request):
    return render(request, 'council/member/index.html')