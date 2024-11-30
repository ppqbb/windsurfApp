from django.db import models
from accounts.models import User, CompanyProfile
from jobs.models import Job, JobApplication

# Create your models here.

class Notification(models.Model):
    NOTIFICATION_TYPES = (
        ('application_status', 'Application Status Change'),
        ('new_job', 'New Job Posted'),
        ('job_deadline', 'Job Deadline Approaching'),
        ('company_response', 'Company Response'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    title = models.CharField(max_length=200)
    message = models.TextField()
    related_job = models.ForeignKey(Job, on_delete=models.SET_NULL, null=True, blank=True)
    related_application = models.ForeignKey(JobApplication, on_delete=models.SET_NULL, null=True, blank=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.title} for {self.user.email}"

class JobAlert(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='job_alerts')
    keywords = models.CharField(max_length=200, blank=True)
    job_types = models.CharField(max_length=100, blank=True)
    locations = models.CharField(max_length=200, blank=True)
    experience_levels = models.CharField(max_length=100, blank=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"Job Alert for {self.user.email}"

class CompanyAnalytics(models.Model):
    company = models.OneToOneField(CompanyProfile, on_delete=models.CASCADE, related_name='analytics')
    total_job_views = models.IntegerField(default=0)
    total_applications = models.IntegerField(default=0)
    average_response_time = models.DurationField(null=True, blank=True)
    acceptance_rate = models.FloatField(default=0)
    last_updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Analytics for {self.company.company_name}"

class JobAnalytics(models.Model):
    job = models.OneToOneField(Job, on_delete=models.CASCADE, related_name='analytics')
    views = models.IntegerField(default=0)
    applications = models.IntegerField(default=0)
    shortlisted = models.IntegerField(default=0)
    rejected = models.IntegerField(default=0)
    last_updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Analytics for {self.job.title}"
