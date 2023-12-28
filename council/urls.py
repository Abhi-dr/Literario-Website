from django.contrib import admin
from django.urls import path

from . import views
from . import president_views 
from . import finance_views

urlpatterns = [
    path('', views.index, name='council'),
    path("member", views.member, name='member'),
    path("my_profile", views.my_profile, name='my_profile'),
    path("update_profile", views.update_profile, name='update_profile'),
    path("change_password", views.change_password, name='change_password'),
    
    
    # ============================= PRESIDENT =================================
    
    path('president', president_views.president, name='president'),
    path("my_council", president_views.my_council, name='my_council'),
    path("president_my_profile", president_views.president_my_profile, name='president_my_profile'),
    path("president_update_profile", president_views.president_update_profile, name='president_update_profile'),
    
    # ============================== FINANCE ==================================
    
    path("approve_registrations", finance_views.approve_registrations, name='approve_registrations'),
    path("approve_registration/<int:registration_id>", finance_views.approve_registration, name='approve_registration'),
    path("reject_registration/<int:registration_id>", finance_views.reject_registration, name='reject_registration'),
]
