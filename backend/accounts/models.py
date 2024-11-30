from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

class User(AbstractUser):
    USER_TYPE_CHOICES = (
        ('applicant', 'Applicant'),
        ('company', 'Company'),
        ('admin', 'Admin'),
    )
    
    email = models.EmailField(_('email address'), unique=True)
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)
    phone_number = models.CharField(max_length=15, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'user_type']

class ApplicantProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='applicant_profile')
    resume = models.FileField(upload_to='resumes/', blank=True)
    skills = models.TextField(blank=True)
    experience = models.TextField(blank=True)
    education = models.TextField(blank=True)
    preferred_job_categories = models.TextField(blank=True)
    preferred_locations = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.user.email}'s Profile"

class CompanyProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='company_profile')
    company_name = models.CharField(max_length=100)
    description = models.TextField()
    website = models.URLField(blank=True)
    industry = models.CharField(max_length=50)
    company_size = models.CharField(max_length=50)
    founded_year = models.IntegerField(null=True, blank=True)
    logo = models.ImageField(upload_to='company_logos/', blank=True)
    subscription_type = models.CharField(
        max_length=10,
        choices=(('standard', 'Standard'), ('premium', 'Premium')),
        default='standard'
    )
    
    def __str__(self):
        return self.company_name
