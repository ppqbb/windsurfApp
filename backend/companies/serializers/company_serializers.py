from rest_framework import serializers
from companies.models import (
    Notification, JobAlert, CompanyAnalytics, JobAnalytics
)
from jobs.serializers.job_serializers import JobSerializer
from accounts.serializers.user_serializers import UserSerializer

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ('id', 'user', 'notification_type', 'title', 'message',
                 'related_job', 'related_application', 'is_read', 'created_at')
        read_only_fields = ('id', 'created_at')

class JobAlertSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobAlert
        fields = ('id', 'user', 'keywords', 'job_types', 'locations',
                 'experience_levels', 'is_active')
        read_only_fields = ('id',)

class CompanyAnalyticsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyAnalytics
        fields = ('id', 'company', 'total_job_views', 'total_applications',
                 'average_response_time', 'acceptance_rate', 'last_updated')
        read_only_fields = ('id', 'last_updated')

class JobAnalyticsSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobAnalytics
        fields = ('id', 'job', 'views', 'applications', 'shortlisted',
                 'rejected', 'last_updated')
        read_only_fields = ('id', 'last_updated')
