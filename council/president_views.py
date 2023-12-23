from django.shortcuts import render, redirect
from .decorators import admin_only

@admin_only
def president(request):
    return render(request, 'council/president/index.html')
    
