from django.shortcuts import render, redirect

def home(request):
    return render(request, 'home/index.html')

def about(request):
    return render(request, 'home/about.html')

def contact(request):
    return render(request, 'home/contact.html')

def events(request):
    return render(request, 'home/events.html')

def videos(request):
    return render(request, 'home/videos.html')

