from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import Job
from .serializers import JobSerializer
from .services import JobSearchService
from django.db.models import Q

class JobViewSet(viewsets.ModelViewSet):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'])
    def search(self, request):
        """
        Advanced search endpoint with multiple filters and sorting options
        """
        search_params = {
            'keywords': request.query_params.get('keywords'),
            'location': request.query_params.get('location'),
            'jobType': request.query_params.getlist('jobType[]', []),
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

# Create your views here.
