from django.db import models
from django.utils import timezone
from accounts.models import User, CompanyProfile
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.

class JobCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    
    def __str__(self):
        return self.name

class Job(models.Model):
    EMPLOYMENT_TYPE_CHOICES = [
        ('FULL_TIME', 'Full-time'),
        ('PART_TIME', 'Part-time'),
        ('CONTRACT', 'Contract'),
        ('INTERNSHIP', 'Internship'),
        ('REMOTE', 'Remote'),
    ]

    EXPERIENCE_LEVEL_CHOICES = [
        ('ENTRY', 'Entry'),
        ('MID_LEVEL', 'Mid-Level'),
        ('SENIOR', 'Senior'),
        ('LEAD', 'Lead'),
        ('MANAGER', 'Manager'),
    ]

    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('pending', 'Pending Approval'),
        ('active', 'Active'),
        ('closed', 'Closed'),
    )
    
    company = models.ForeignKey(CompanyProfile, on_delete=models.CASCADE, related_name='jobs')
    title = models.CharField(max_length=200, db_index=True)
    description = models.TextField(blank=True, default='')
    requirements = models.TextField(blank=True, default='')
    responsibilities = models.TextField(blank=True, default='')
    category = models.ForeignKey(JobCategory, on_delete=models.SET_NULL, null=True)
    location = models.CharField(max_length=200, db_index=True)
    salary_min = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    salary_max = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    employment_type = models.CharField(max_length=20, choices=EMPLOYMENT_TYPE_CHOICES, default='FULL_TIME', db_index=True)
    experience_level = models.CharField(max_length=20, choices=EXPERIENCE_LEVEL_CHOICES, default='ENTRY', db_index=True)
    skills_required = models.TextField(blank=True, default='')  # Store as comma-separated values
    is_remote = models.BooleanField(default=False, db_index=True)
    has_equity = models.BooleanField(default=False, db_index=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft', db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)
    deadline = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True, db_index=True)
    views_count = models.PositiveIntegerField(default=0)
    applications_count = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} at {self.company.company_name}"

    def update_counts(self):
        self.views_count = self.job_views.count()
        self.applications_count = self.applications.count()
        self.save()

class JobApplication(models.Model):
    STATUS_CHOICES = (
        ('submitted', 'Submitted'),
        ('under_review', 'Under Review'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    )
    
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applications')
    applicant = models.ForeignKey(User, on_delete=models.CASCADE, related_name='applications')
    cover_letter = models.TextField(blank=True)
    resume = models.FileField(upload_to='job_applications/resumes/', blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='submitted')
    applied_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('job', 'applicant')
    
    def __str__(self):
        return f"{self.applicant.email}'s application for {self.job.title}"

class CustomApplicationQuestion(models.Model):
    QUESTION_TYPE_CHOICES = (
        ('text', 'Text'),
        ('number', 'Number'),
        ('choice', 'Multiple Choice'),
        ('boolean', 'Yes/No'),
    )
    
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='custom_questions')
    question_type = models.CharField(max_length=10, choices=QUESTION_TYPE_CHOICES)
    question_text = models.CharField(max_length=500)
    choices = models.TextField(blank=True, help_text='Comma-separated choices for multiple choice questions')
    is_required = models.BooleanField(default=True)
    
    def __str__(self):
        return f"Question for {self.job.title}"

class ApplicationAnswer(models.Model):
    application = models.ForeignKey(JobApplication, on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey(CustomApplicationQuestion, on_delete=models.CASCADE)
    answer = models.TextField()
    
    def __str__(self):
        return f"Answer for {self.question.question_text}"
