from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.utils import timezone

from accounts.models import Profile

class Event(models.Model):
    name = models.CharField(max_length=200)
    date = models.DateTimeField('date published')
    description = models.TextField()
    latest_update = models.TextField(blank=True, null=True)
    ticket_price = models.IntegerField(default=0)
    total_tickets = models.IntegerField(default=0)
    thumbnail = models.ImageField(upload_to='events/thumbnails', default='events/thumbnails/default.png')
    slug = models.SlugField(max_length=200, unique=True)  # New slug field
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('events:detail', kwargs={'slug': self.slug})
    
    def get_current_status_based_on_time(self):
        if self.date > timezone.now():
            return "Upcoming"
        else:
            return "Past"
        
    def get_current_status_based_on_tickets(self):
        if self.total_tickets > 0:
            return "Available"
        else:
            return "Sold Out"
    
    def save(self, *args, **kwargs):
        # Automatically generate and save the slug based on the event name
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)
# ===================================== Registration ==================================

class Registration(models.Model):
    
    YEAR_CHOICES = (
        ('1st Year', '1st Year'),
        ('2nd Year', '2nd Year'),
        ('3rd Year', '3rd Year'),
        ('4th Year', '4th Year'),
    )
    
    COURSE_CHOICES = [
        ('B.Tech', 'B.Tech'),
        ('BCA', 'BCA'),
        ('BBA', 'BBA'),
        ('MBA', 'MBA'),
        ('BA', 'BA')
    ]
    
    GENDER_CHOICES = [
        ("Male", "Male"),
        ("Female", "Female"),
        ("Other", "Other"),
    ]
    
    D_H_CHOICES = [
        ("Day Scholar", "Day Scholar"),
        ("Hosteller", "Hosteller"),
    ]
    
    name = models.CharField(max_length=255)
    course = models.CharField(max_length=20, choices=COURSE_CHOICES, default='B.Tech')
    year = models.CharField(max_length=20, choices=YEAR_CHOICES, default='1st Year')
    email = models.EmailField()
    hosteller_dayScholar = models.CharField(max_length=20, choices=D_H_CHOICES, default='Day Scholar')
    
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    
    referral_name = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=True)
    
    referral_code = models.CharField(max_length=10, null=True, blank=True)
    
    other_referral_name = models.CharField(max_length=255, null=True, blank=True)
    
    payment_screenshot = models.ImageField(upload_to='events/payment_screenshots', null=True, blank=True)
    referrance_number = models.CharField(max_length=20, null=True, blank=True)
    
    approved_by_head = models.BooleanField(default=False)
    
    is_present = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} - {self.event.name}"
    
    def save(self, *args, **kwargs):
        if self.referral_name:
            self.referral_code = self.referral_name.referral_code
        super().save(*args, **kwargs)
        
    def get_approved_status(self):
        if self.approved_by_head:
            return "green"
        else:
            return "red"
    
    def get_approved_status_text(self):
        if self.approved_by_head:
            return "Approved"
        else:
            return "Not Approved"