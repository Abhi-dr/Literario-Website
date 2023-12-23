from django.db import models
from django.contrib.auth.models import User, Group

class Profile(User):
    POST_CHOICES = [
        ('President', 'President'),
        ('Vice President', 'Vice President'),
        ('General Secretary', 'General Secretary'),
        ("Joint Secretary", "Joint Secretary"),
        ("Treasurer", "Treasurer"),
        ("Curator", "Curator"),
        ('Head', 'Head'),
        ('Deputy Head', 'Deputy Head'),
        ("Associate", "Associate"),
        ('Member', 'Member'),
    ]
    
    YEAR_CHOICES = (
        ('1st Year', '1st Year'),
        ('2nd Year', '2nd Year'),
        ('3rd Year', '3rd Year'),
        ('4th Year', '4th Year'),
    )
    
    TEAM_CHOICES = [
        ('Technical Team', 'Technical Team'),
        ("Event Management Team", "Event Management Team"),
        ("Corporate Relations (CR) Team", "Corporate Relations (CR) Team"),
        ("Creative Team", "Creative Team"),
        ("Data Team", "Data Team"),
        ("Design Team", "Design Team"),
        ("Editoral Team", "Editoral Team"),
        ("Finance Team", "Finance Team"),
        ("Public Relations (PR) Team", "Public Relations (PR) Team"),
    ]
    
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

    course = models.CharField(max_length=20, choices=COURSE_CHOICES, default='B.Tech')
    year = models.CharField(max_length=20, choices=YEAR_CHOICES, default='1st Year')
    team = models.CharField(max_length=50, choices=TEAM_CHOICES, default='Technical Team')
    post = models.CharField(max_length=20, choices=POST_CHOICES, default='Member')
    gender = models.CharField(choices = GENDER_CHOICES, default = "Male", max_length=10)
    mobile_number = models.IntegerField()

    profile_pic = models.FileField(upload_to="images", blank=True, null=True)
    
    def __str__(self):
        return f"{self.first_name}"
    
    def save(self, *args, **kwargs):
        if not self.pk:
            self.is_staff = False
            self.set_password('iloveliterario')
        super().save(*args, **kwargs)
        
    class Meta:
        verbose_name = "Profile"
        verbose_name_plural = "Profiles"

