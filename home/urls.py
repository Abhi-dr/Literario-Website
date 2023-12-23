from django.contrib import admin
from django.urls import path, include

from . import views

urlpatterns = [
    
    path('', views.home, name="home"),
    path('about/', views.about, name="about"),
    path('contact/', views.contact, name="contact"),
    path('events', views.events, name="events"),
    path('videos/', views.videos, name="videos"),
    
]
