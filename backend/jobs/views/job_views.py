from rest_framework import viewsets, status, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from jobs.models import (
    JobCategory, Job, JobApplication,
    CustomApplicationQuestion, ApplicationAnswer
)
from jobs.serializers import (
    JobCategorySerializer,
    JobSerializer,
    JobListSerializer,
    JobApplicationSerializer,
    JobApplicationCreateSerializer,
    CustomApplicationQuestionSerializer,
)

class JobCategoryViewSet(viewsets.ModelViewSet):
    queryset = JobCategory.objects.all()
    serializer_class = JobCategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class JobViewSet(viewsets.ModelViewSet):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'job_type', 'experience_level', 'location', 'status']
    search_fields = ['title', 'description', 'company__company_name']
    ordering_fields = ['created_at', 'deadline']

    def get_serializer_class(self):
        if self.action == 'list':
            return JobListSerializer
        return JobSerializer

    def perform_create(self, serializer):
        company_profile = self.request.user.company_profile
        serializer.save(company=company_profile, status='pending')

    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        job = self.get_object()
        if request.user.user_type != 'admin':
            return Response(
                {'error': 'Only admin can approve jobs'},
                status=status.HTTP_403_FORBIDDEN
            )
        job.status = 'active'
        job.save()
        return Response({'status': 'job approved'})

class JobApplicationViewSet(viewsets.ModelViewSet):
    serializer_class = JobApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.user_type == 'applicant':
            return JobApplication.objects.filter(applicant=user)
        elif user.user_type == 'company':
            return JobApplication.objects.filter(job__company__user=user)
        return JobApplication.objects.all()

    def get_serializer_class(self):
        if self.action == 'create':
            return JobApplicationCreateSerializer
        return JobApplicationSerializer

    def perform_create(self, serializer):
        serializer.save(applicant=self.request.user)

    @action(detail=True, methods=['post'])
    def update_status(self, request, pk=None):
        application = self.get_object()
        new_status = request.data.get('status')
        if new_status not in dict(JobApplication.STATUS_CHOICES):
            return Response(
                {'error': 'Invalid status'},
                status=status.HTTP_400_BAD_REQUEST
            )
        application.status = new_status
        application.save()
        return Response({'status': 'application status updated'})
