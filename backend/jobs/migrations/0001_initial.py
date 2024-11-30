# Generated by Django 4.2.7 on 2024-11-30 18:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('requirements', models.TextField()),
                ('job_type', models.CharField(choices=[('full_time', 'Full Time'), ('part_time', 'Part Time'), ('contract', 'Contract'), ('internship', 'Internship')], max_length=20)),
                ('experience_level', models.CharField(choices=[('entry', 'Entry Level'), ('mid', 'Mid Level'), ('senior', 'Senior Level'), ('lead', 'Lead'), ('manager', 'Manager')], max_length=20)),
                ('location', models.CharField(max_length=100)),
                ('salary_range', models.CharField(blank=True, max_length=100)),
                ('status', models.CharField(choices=[('draft', 'Draft'), ('pending', 'Pending Approval'), ('active', 'Active'), ('closed', 'Closed')], default='draft', max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deadline', models.DateTimeField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='JobCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='JobApplication',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cover_letter', models.TextField(blank=True)),
                ('resume', models.FileField(blank=True, upload_to='job_applications/resumes/')),
                ('status', models.CharField(choices=[('submitted', 'Submitted'), ('under_review', 'Under Review'), ('accepted', 'Accepted'), ('rejected', 'Rejected')], default='submitted', max_length=20)),
                ('applied_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('applicant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='applications', to=settings.AUTH_USER_MODEL)),
                ('job', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='applications', to='jobs.job')),
            ],
            options={
                'unique_together': {('job', 'applicant')},
            },
        ),
        migrations.AddField(
            model_name='job',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='jobs.jobcategory'),
        ),
        migrations.AddField(
            model_name='job',
            name='company',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='jobs', to='accounts.companyprofile'),
        ),
        migrations.CreateModel(
            name='CustomApplicationQuestion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_type', models.CharField(choices=[('text', 'Text'), ('number', 'Number'), ('choice', 'Multiple Choice'), ('boolean', 'Yes/No')], max_length=10)),
                ('question_text', models.CharField(max_length=500)),
                ('choices', models.TextField(blank=True, help_text='Comma-separated choices for multiple choice questions')),
                ('is_required', models.BooleanField(default=True)),
                ('job', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='custom_questions', to='jobs.job')),
            ],
        ),
        migrations.CreateModel(
            name='ApplicationAnswer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer', models.TextField()),
                ('application', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answers', to='jobs.jobapplication')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jobs.customapplicationquestion')),
            ],
        ),
    ]
