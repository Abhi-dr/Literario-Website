from django.contrib import admin

from .models import Profile

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    exclude = ("last_login", "password",  "date_joined", "is_active", "user_permissions", "groups")
    list_display = ("username", "first_name", "last_name", "team", "post")