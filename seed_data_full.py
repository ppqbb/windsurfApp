import os
import django
from django.utils import timezone
from datetime import timedelta
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from accounts.models import User, ApplicantProfile, CompanyProfile
from jobs.models import JobCategory, Job, JobApplication, CustomApplicationQuestion
from companies.models import CompanyAnalytics, JobAnalytics, Notification, JobAlert

def create_sample_data():
    print("Creating sample data...")
    
    # Create job categories
    categories = [
        {"name": "Software Development", "description": "Software development and engineering positions"},
        {"name": "Data Science", "description": "Data science, analytics, and machine learning roles"},
        {"name": "Design", "description": "UI/UX and graphic design positions"},
        {"name": "Marketing", "description": "Digital marketing and social media roles"},
        {"name": "Sales", "description": "Sales and business development positions"},
        {"name": "Customer Service", "description": "Customer support and service roles"},
        {"name": "Project Management", "description": "Project and product management positions"},
        {"name": "Human Resources", "description": "HR and recruitment roles"}
    ]
    
    for cat in categories:
        JobCategory.objects.get_or_create(name=cat["name"], defaults={"description": cat["description"]})
    
    # Create company users and profiles
    companies_data = [
        {
            "email": "company@example.com",
            "password": "company12345",
            "username": "techcorp",
            "company_name": "TechCorp Solutions",
            "description": "Leading technology solutions provider",
            "industry": "Technology",
            "company_size": "100-500"
        },
        {
            "email": "innovate@example.com",
            "password": "company12345",
            "username": "innovate",
            "company_name": "Innovate AI",
            "description": "AI and machine learning solutions",
            "industry": "Artificial Intelligence",
            "company_size": "50-100"
        },
        {
            "email": "design@example.com",
            "password": "company12345",
            "username": "designstudio",
            "company_name": "Design Studio Pro",
            "description": "Creative design agency",
            "industry": "Design",
            "company_size": "10-50"
        }
    ]
    
    for comp_data in companies_data:
        user = User.objects.create_user(
            email=comp_data["email"],
            username=comp_data["username"],
            password=comp_data["password"],
            user_type="company"
        )
        CompanyProfile.objects.create(
            user=user,
            company_name=comp_data["company_name"],
            description=comp_data["description"],
            industry=comp_data["industry"],
            company_size=comp_data["company_size"]
        )
    
    # Create applicant users and profiles
    applicants_data = [
        {
            "email": "user@example.com",
            "password": "user123456",
            "username": "johndoe",
            "first_name": "John",
            "last_name": "Doe",
            "skills": "Python, JavaScript, React\nSQL, MongoDB\nAWS, Docker",
            "experience": "Senior Software Engineer at TechCorp (2018-2023)\nFull Stack Developer at WebSolutions (2015-2018)",
            "education": "Master's in Computer Science, Stanford University\nBachelor's in Software Engineering, MIT"
        },
        {
            "email": "jane@example.com",
            "password": "user123456",
            "username": "janesmith",
            "first_name": "Jane",
            "last_name": "Smith",
            "skills": "UI/UX Design, Figma\nProduct Design\nUser Research",
            "experience": "Product Designer at DesignCo (2019-2023)\nUI Designer at CreativeSolutions (2017-2019)",
            "education": "Bachelor's in Design, Rhode Island School of Design"
        },
        {
            "email": "bob@example.com",
            "password": "user123456",
            "username": "bobwilson",
            "first_name": "Bob",
            "last_name": "Wilson",
            "skills": "Data Science, Python\nMachine Learning\nTensorFlow, PyTorch",
            "experience": "Data Scientist at AITech (2020-2023)\nML Engineer at DataCorp (2018-2020)",
            "education": "PhD in Machine Learning, UC Berkeley\nMaster's in Statistics, UCLA"
        }
    ]
    
    for app_data in applicants_data:
        user = User.objects.create_user(
            email=app_data["email"],
            username=app_data["username"],
            password=app_data["password"],
            first_name=app_data["first_name"],
            last_name=app_data["last_name"],
            user_type="applicant"
        )
        ApplicantProfile.objects.create(
            user=user,
            skills=app_data["skills"],
            experience=app_data["experience"],
            education=app_data["education"]
        )
    
    # Create admin user
    User.objects.create_superuser(
        email="admin@example.com",
        username="admin",
        password="admin12345",
        user_type="admin"
    )
    
    # Create jobs
    job_titles = [
        "Senior Software Engineer",
        "Data Scientist",
        "UI/UX Designer",
        "Product Manager",
        "Full Stack Developer",
        "Machine Learning Engineer",
        "DevOps Engineer",
        "Frontend Developer",
        "Backend Developer",
        "Mobile App Developer"
    ]
    
    job_types = ["Full-time", "Part-time", "Contract", "Remote"]
    experience_levels = ["Entry", "Mid-level", "Senior", "Lead"]
    locations = ["New York", "San Francisco", "London", "Berlin", "Tokyo", "Remote"]
    
    companies = CompanyProfile.objects.all()
    categories = JobCategory.objects.all()
    
    for _ in range(20):  # Create 20 jobs
        company = random.choice(companies)
        category = random.choice(categories)
        
        job = Job.objects.create(
            company=company,
            title=random.choice(job_titles),
            description=f"We are looking for a talented professional to join our team...",
            requirements="- 5+ years of experience\n- Strong problem-solving skills\n- Excellent communication",
            responsibilities="- Develop and maintain software applications\n- Collaborate with team members\n- Write clean, efficient code",
            category=category,
            employment_type=random.choice(['FULL_TIME', 'PART_TIME', 'CONTRACT', 'REMOTE']),
            experience_level=random.choice(['ENTRY', 'MID_LEVEL', 'SENIOR', 'LEAD', 'MANAGER']),
            location=random.choice(locations),
            salary_min=random.randint(50000, 100000),
            salary_max=random.randint(100001, 150000),
            skills_required="Python, JavaScript, React, SQL",
            is_remote=random.choice([True, False]),
            deadline=timezone.now() + timedelta(days=random.randint(7, 30))
        )
        
        # Create custom questions for each job
        questions = [
            {"text": "Why do you want to work with us?", "type": "text"},
            {"text": "What are your salary expectations?", "type": "text"},
            {"text": "When can you start?", "type": "text"}
        ]
        
        for q in questions:
            CustomApplicationQuestion.objects.create(
                job=job,
                question_text=q["text"],
                question_type=q["type"],
                is_required=True
            )
    
    # Create job applications
    jobs = Job.objects.all()
    applicants = User.objects.filter(user_type="applicant")
    
    for applicant in applicants:
        # Get random jobs without replacement
        random_jobs = random.sample(list(jobs), min(random.randint(2, 5), len(jobs)))
        for job in random_jobs:
            status = random.choice(["submitted", "under_review", "accepted", "rejected"])
            
            JobApplication.objects.create(
                job=job,
                applicant=applicant,
                cover_letter="I am very interested in this position...",
                status=status,
                applied_at=timezone.now() - timedelta(days=random.randint(1, 30))
            )
    
    # Create company analytics
    for company in companies:
        CompanyAnalytics.objects.create(
            company=company,
            total_job_views=random.randint(1000, 5000),
            total_applications=random.randint(100, 500),
            average_response_time=timedelta(days=random.randint(1, 7)),
            acceptance_rate=random.uniform(0.1, 0.3)
        )
    
    # Create job analytics
    for job in jobs:
        JobAnalytics.objects.create(
            job=job,
            views=random.randint(100, 1000),
            applications=random.randint(10, 50),
            shortlisted=random.randint(5, 20),
            rejected=random.randint(5, 20)
        )
    
    # Create notifications
    for user in User.objects.all():
        for _ in range(random.randint(2, 5)):
            notification_types = ["application_status", "new_job", "profile_view"]
            Notification.objects.create(
                user=user,
                notification_type=random.choice(notification_types),
                title="New Notification",
                message="You have a new update in your account...",
                is_read=random.choice([True, False])
            )
    
    # Create job alerts
    for applicant in applicants:
        JobAlert.objects.create(
            user=applicant,
            keywords="python, javascript",
            job_types=random.choice(job_types),
            locations=random.choice(locations),
            experience_levels=random.choice(experience_levels)
        )
    
    print("Sample data creation completed!")

if __name__ == "__main__":
    create_sample_data()
