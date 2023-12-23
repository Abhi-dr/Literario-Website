from django.contrib import admin
from django.urls import path

from . import views
from . import president_views 

urlpatterns = [
    path('', views.index, name='council'),
    path("member", views.member, name='member'),
    
    
    
    # ============================= PRESIDENT =================================
    
    path('president', president_views.president, name='president'),
]
