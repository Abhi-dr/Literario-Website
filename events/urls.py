from django.contrib import admin
from django.urls import path

from . import views


urlpatterns = [
    path("registration", views.registration, name="registration"),
    # path('paymenthandler/', views.paymenthandler, name='paymenthandler'),
    
    # path("teri_maa_ka_bharosa", views.all_events, name="teri_maa_ka_bharosa"),    
        
]
