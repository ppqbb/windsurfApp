from django.contrib.auth import get_user_model
from accounts.models import ApplicantProfile
from jobs.models import Job, JobApplication
from django.utils import timezone
import random

User = get_user_model()

def create_sample_data():
    # Create sample users
    users = [
        {
            'email': 'admin@example.com',
            'password': 'admin12345',
            'is_staff': True,
            'is_superuser': True,
            'username': 'admin',
            'user_type': 'admin'
        },
        {
            'email': 'company@example.com',
            'password': 'company12345',
            'username': 'company',
            'user_type': 'company'
        },
        {
            'email': 'user@example.com',
            'password': 'user123456',
            'username': 'user',
            'user_type': 'applicant'
        }
    ]

    created_users = []
    for user_data in users:
        user = User.objects.create_user(
            email=user_data['email'],
            password=user_data['password'],
            username=user_data['username'],
            user_type=user_data['user_type']
        )
        if user_data.get('is_staff'):
            user.is_staff = True
            user.is_superuser = True
            user.save()
        created_users.append(user)

    # Create applicant profile
    applicant = created_users[2]  # user@example.com
    ApplicantProfile.objects.create(
        user=applicant,
        skills='Python, JavaScript, React, Django',
        experience='5 years of software development experience',
        education='Bachelor in Computer Science',
        preferred_job_categories='Software Development, Web Development',
        preferred_locations='Remote, New York, San Francisco'
    )

    # Create sample jobs
    job_titles = [
        'Senior Software Engineer',
        'UI/UX Designer',
        'Data Scientist',
        'Product Manager',
        'Frontend Developer',
        'Backend Developer',
        'DevOps Engineer',
        'Marketing Manager'
    ]

    company_user = created_users[1]  # company@example.com
    
    for title in job_titles[:3]:  # Create 3 jobs
        Job.objects.create(
            company=company_user,
            title=title,
            description='Lorem ipsum dolor sit amet, consectetur adipiscing elit.',
            requirements='- 3+ years of experience\n- Bachelor\'s degree\n- Strong communication skills',
            salary_range='$80,000 - $120,000',
            location='Remote',
            job_type=random.choice(['FULL_TIME', 'PART_TIME', 'CONTRACT']),
            experience_level=random.choice(['ENTRY', 'MID', 'SENIOR']),
            status='ACTIVE'
        )

    # Create sample applications
    applicant_user = created_users[2]  # user@example.com
    for job in Job.objects.all():
        JobApplication.objects.create(
            job=job,
            applicant=applicant_user,
            cover_letter='I am very interested in this position...',
            status=random.choice(['PENDING', 'REVIEWING', 'ACCEPTED', 'REJECTED']),
            application_date=timezone.now()
        )

if __name__ == '__main__':
    create_sample_data()
