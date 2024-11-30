from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from companies.models import (
    Notification, JobAlert, CompanyAnalytics, JobAnalytics
)
from companies.serializers import (
    NotificationSerializer,
    JobAlertSerializer,
    CompanyAnalyticsSerializer,
    JobAnalyticsSerializer,
)

class NotificationViewSet(viewsets.ModelViewSet):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user)

    @action(detail=True, methods=['post'])
    def mark_as_read(self, request, pk=None):
        notification = self.get_object()
        notification.is_read = True
        notification.save()
        return Response({'status': 'notification marked as read'})

    @action(detail=False, methods=['post'])
    def mark_all_as_read(self, request):
        self.get_queryset().update(is_read=True)
        return Response({'status': 'all notifications marked as read'})

class JobAlertViewSet(viewsets.ModelViewSet):
    serializer_class = JobAlertSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return JobAlert.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class CompanyAnalyticsViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = CompanyAnalyticsSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.user_type == 'company':
            return CompanyAnalytics.objects.filter(company__user=user)
        elif user.user_type == 'admin':
            return CompanyAnalytics.objects.all()
        return CompanyAnalytics.objects.none()

class JobAnalyticsViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = JobAnalyticsSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.user_type == 'company':
            return JobAnalytics.objects.filter(job__company__user=user)
        elif user.user_type == 'admin':
            return JobAnalytics.objects.all()
        return JobAnalytics.objects.none()
