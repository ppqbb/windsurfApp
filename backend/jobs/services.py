from django.db.models import Q
from datetime import datetime, timedelta
from .models import Job

class JobSearchService:
    @staticmethod
    def search_jobs(params):
        queryset = Job.objects.filter(is_active=True)
        
        # Basic text search
        if params.get('keywords'):
            keywords = params['keywords']
            queryset = queryset.filter(
                Q(title__icontains=keywords) |
                Q(description__icontains=keywords) |
                Q(requirements__icontains=keywords) |
                Q(company__name__icontains=keywords)
            )

        # Location filter
        if params.get('location'):
            queryset = queryset.filter(
                Q(location__icontains=params['location']) |
                Q(is_remote=True)
            )

        # Job type filter
        if params.get('jobType'):
            queryset = queryset.filter(employment_type__in=params['jobType'])

        # Experience level filter
        if params.get('experienceLevel'):
            queryset = queryset.filter(experience_level__in=params['experienceLevel'])

        # Salary range filter
        if params.get('salary'):
            min_salary, max_salary = params['salary']
            queryset = queryset.filter(
                Q(salary_min__gte=min_salary) |
                Q(salary_max__lte=max_salary)
            )

        # Skills filter
        if params.get('skills'):
            for skill in params['skills']:
                queryset = queryset.filter(skills_required__icontains=skill)

        # Posted date filter
        if params.get('postedDate'):
            posted_date = datetime.strptime(params['postedDate'], '%Y-%m-%d')
            queryset = queryset.filter(created_at__gte=posted_date)

        # Remote work filter
        if params.get('remote'):
            queryset = queryset.filter(is_remote=True)

        # Equity filter
        if params.get('hasEquity'):
            queryset = queryset.filter(has_equity=True)

        # Company size filter
        if params.get('companySize'):
            queryset = queryset.filter(
                company__employee_count__range=params['companySize']
            )

        # Industry filter
        if params.get('industry'):
            queryset = queryset.filter(company__industry__in=params['industry'])

        # Sorting
        sort_by = params.get('sortBy', 'date')
        sort_order = params.get('sortOrder', 'desc')

        if sort_by == 'date':
            queryset = queryset.order_by(
                '-created_at' if sort_order == 'desc' else 'created_at'
            )
        elif sort_by == 'salary':
            queryset = queryset.order_by(
                '-salary_max' if sort_order == 'desc' else 'salary_max'
            )

        # Pagination
        page = int(params.get('page', 1))
        limit = int(params.get('limit', 10))
        start = (page - 1) * limit
        end = start + limit

        total = queryset.count()
        jobs = queryset[start:end]

        return {
            'total': total,
            'jobs': jobs,
            'page': page,
            'pages': (total + limit - 1) // limit,
            'limit': limit
        }

    @staticmethod
    def get_suggestions(query, type):
        if type == 'skills':
            return Job.objects.filter(
                skills_required__icontains=query
            ).values_list(
                'skills_required', flat=True
            ).distinct()[:10]
        
        elif type == 'companies':
            return Job.objects.filter(
                company__name__icontains=query
            ).values_list(
                'company__name', flat=True
            ).distinct()[:10]
        
        elif type == 'locations':
            return Job.objects.filter(
                location__icontains=query
            ).values_list(
                'location', flat=True
            ).distinct()[:10]

    @staticmethod
    def get_similar_jobs(job_id, limit=5):
        job = Job.objects.get(id=job_id)
        
        similar_jobs = Job.objects.filter(
            Q(skills_required__overlap=job.skills_required) |
            Q(title__icontains=job.title) |
            Q(experience_level=job.experience_level)
        ).exclude(
            id=job_id
        ).distinct()

        # Calculate similarity score
        similar_jobs = similar_jobs.annotate(
            similarity_score=Greatest(
                F('skills_required__overlap'),
                F('title__similarity'),
                F('experience_level__similarity')
            )
        ).order_by('-similarity_score')[:limit]

        return similar_jobs

    @staticmethod
    def get_popular_searches():
        # This could be implemented with Redis or another caching system
        # For now, return some dummy data
        return [
            {'query': 'Software Engineer', 'count': 1000},
            {'query': 'Data Scientist', 'count': 800},
            {'query': 'Product Manager', 'count': 600},
            {'query': 'DevOps Engineer', 'count': 500},
            {'query': 'UI/UX Designer', 'count': 400},
        ]
