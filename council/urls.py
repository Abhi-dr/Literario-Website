from django.contrib import admin
from django.urls import path

from . import views
from . import president_views 
from . import finance_views

urlpatterns = [
    path('', views.index, name='council'),
    path("member", views.member, name='member'),
    path("my_profile", views.my_profile, name='my_profile'),
    
    
    # ============================= PRESIDENT =================================
    
    path('president', president_views.president, name='president'),
    
    # ============================== FINANCE ==================================
    
    path("approve_registrations", finance_views.approve_registrations, name='approve_registrations'),
    path("approve_registration/<int:registration_id>", finance_views.approve_registration, name='approve_registration'),
    path("reject_registration/<int:registration_id>", finance_views.reject_registration, name='reject_registration'),
]
