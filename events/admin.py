from django.contrib import admin
from .models import Event, Registration

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'date', 'description', 'ticket_price', 'total_tickets')
    list_filter = ('name', 'ticket_price', 'total_tickets')
    
@admin.register(Registration)
class RegistrarionAdmin(admin.ModelAdmin):
    list_display = ("name", "course", "year", "hosteller_dayScholar", "event", "referral_name")
    list_filter = ("course", "year", "hosteller_dayScholar", "event", "referral_name")