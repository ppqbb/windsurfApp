from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from .models import Job, JobApplication
from .serializers import JobSerializer, JobApplicationSerializer
from .services import JobSearchService
from .filters import JobFilter
from .permissions import IsCompanyOrAdmin, IsCompanyWithinJobLimit, IsAdmin, IsApplicant
from django.db.models import Q

class JobViewSet(viewsets.ModelViewSet):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = JobFilter
    search_fields = ['title', 'description', 'requirements', 'responsibilities', 'skills_required']
    ordering_fields = ['created_at', 'deadline', 'salary_min', 'salary_max']
    ordering = ['-created_at']

    def get_permissions(self):
        if self.action in ['create']:
            return [IsAuthenticated(), IsCompanyWithinJobLimit()]
        if self.action in ['update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), IsCompanyOrAdmin()]
        if self.action in ['approve', 'reject']:
            return [IsAuthenticated(), IsAdmin()]
        return [IsAuthenticated()]

    def perform_create(self, serializer):
        serializer.save(
            company=self.request.user.company_profile,
            status='pending' if self.request.user.user_type == 'company' else 'active'
        )

    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        job = self.get_object()
        if job.status != 'pending':
            return Response(
                {'detail': 'Only pending jobs can be approved'},
                status=status.HTTP_400_BAD_REQUEST
            )
        job.status = 'active'
        job.save()
        return Response({'status': 'job approved'})

    @action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        job = self.get_object()
        if job.status != 'pending':
            return Response(
                {'detail': 'Only pending jobs can be rejected'},
                status=status.HTTP_400_BAD_REQUEST
            )
        job.status = 'draft'
        job.save()
        return Response({'status': 'job rejected'})

    @action(detail=False, methods=['get'])
    def my_jobs(self, request):
        if request.user.user_type == 'company':
            jobs = Job.objects.filter(company=request.user.company_profile)
        else:
            jobs = Job.objects.none()
        serializer = self.get_serializer(jobs, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def search(self, request):
        """
        Advanced search endpoint with multiple filters and sorting options
        """
        search_params = {
            'keywords': request.query_params.get('keywords'),
            'location': request.query_params.get('location'),
            'employment_type': request.query_params.getlist('employment_type[]', []),
            'experienceLevel': request.query_params.getlist('experienceLevel[]', []),
            'salary': [
                float(request.query_params.get('minSalary', 0)),
                float(request.query_params.get('maxSalary', 1000000))
            ] if request.query_params.get('minSalary') or request.query_params.get('maxSalary') else None,
            'skills': request.query_params.getlist('skills[]', []),
            'postedDate': request.query_params.get('postedDate'),
            'remote': request.query_params.get('remote') == 'true',
            'hasEquity': request.query_params.get('hasEquity') == 'true',
            'companySize': [
                int(request.query_params.get('minSize', 0)),
                int(request.query_params.get('maxSize', 1000000))
            ] if request.query_params.get('minSize') or request.query_params.get('maxSize') else None,
            'industry': request.query_params.getlist('industry[]', []),
            'page': int(request.query_params.get('page', 1)),
            'limit': int(request.query_params.get('limit', 10)),
            'sortBy': request.query_params.get('sortBy', 'date'),
            'sortOrder': request.query_params.get('sortOrder', 'desc'),
        }

        search_results = JobSearchService.search_jobs(search_params)
        serialized_jobs = JobSerializer(search_results['jobs'], many=True).data

        return Response({
            'total': search_results['total'],
            'jobs': serialized_jobs,
            'page': search_results['page'],
            'pages': search_results['pages'],
            'limit': search_results['limit'],
        })

    @action(detail=False, methods=['get'])
    def suggestions(self, request):
        """
        Get search suggestions based on partial input
        """
        query = request.query_params.get('query', '')
        type = request.query_params.get('type', 'skills')
        limit = int(request.query_params.get('limit', 5))

        if type == 'skills':
            suggestions = Job.objects.filter(
                skills_required__icontains=query
            ).values_list('skills_required', flat=True).distinct()[:limit]
        elif type == 'locations':
            suggestions = Job.objects.filter(
                location__icontains=query
            ).values_list('location', flat=True).distinct()[:limit]
        else:
            suggestions = []

        return Response(list(suggestions))

    @action(detail=True, methods=['get'])
    def similar(self, request, pk=None):
        """
        Get similar jobs based on current job
        """
        job = self.get_object()
        limit = int(request.query_params.get('limit', 5))
        
        similar_jobs = Job.objects.filter(
            Q(category=job.category) |
            Q(employment_type=job.employment_type) |
            Q(experience_level=job.experience_level)
        ).exclude(id=job.id).distinct()[:limit]
        
        serialized_jobs = JobSerializer(similar_jobs, many=True).data
        return Response(serialized_jobs)

    @action(detail=False, methods=['get'])
    def popular(self, request):
        """
        Get popular search queries
        """
        popular_searches = JobSearchService.get_popular_searches()
        return Response(popular_searches)

    @action(detail=False, methods=['get'])
    def location(self, request):
        """
        Search jobs by location with radius
        """
        search_params = request.query_params.copy()
        search_params['radius'] = float(request.query_params.get('radius', 50))
        
        search_results = JobSearchService.search_jobs(search_params)
        serialized_jobs = JobSerializer(search_results['jobs'], many=True).data

        return Response({
            'total': search_results['total'],
            'jobs': serialized_jobs,
            'page': search_results['page'],
            'limit': search_results['limit'],
        })

class JobApplicationViewSet(viewsets.ModelViewSet):
    serializer_class = JobApplicationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.user_type == 'applicant':
            return JobApplication.objects.filter(applicant=self.request.user)
        elif self.request.user.user_type == 'company':
            return JobApplication.objects.filter(job__company=self.request.user.company_profile)
        elif self.request.user.user_type == 'admin':
            return JobApplication.objects.all()
        return JobApplication.objects.none()

    def perform_create(self, serializer):
        job = get_object_or_404(Job, id=self.request.data.get('job'))
        if job.status != 'active':
            raise ValidationError('This job is not accepting applications')
        serializer.save(applicant=self.request.user)

    @action(detail=True, methods=['post'])
    def update_status(self, request, pk=None):
        application = self.get_object()
        if request.user.user_type not in ['company', 'admin']:
            return Response(
                {'detail': 'Only companies and admins can update application status'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        new_status = request.data.get('status')
        if new_status not in [s[0] for s in JobApplication.STATUS_CHOICES]:
            return Response(
                {'detail': 'Invalid status'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        application.status = new_status
        application.save()
        return Response({'status': 'application status updated'})

    @action(detail=False, methods=['get'])
    def my_applications(self, request):
        if request.user.user_type != 'applicant':
            return Response(
                {'detail': 'Only applicants can view their applications'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        applications = JobApplication.objects.filter(applicant=request.user)
        serializer = self.get_serializer(applications, many=True)
        return Response(serializer.data)

# Create your views here.
