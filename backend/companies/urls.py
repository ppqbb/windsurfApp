from django.urls import path, include
from rest_framework.routers import DefaultRouter
from companies.views import (
    NotificationViewSet,
    JobAlertViewSet,
    CompanyAnalyticsViewSet,
    JobAnalyticsViewSet,
)

router = DefaultRouter()
router.register(r'notifications', NotificationViewSet, basename='notification')
router.register(r'job-alerts', JobAlertViewSet, basename='job-alert')
router.register(r'company-analytics', CompanyAnalyticsViewSet, basename='company-analytics')
router.register(r'job-analytics', JobAnalyticsViewSet, basename='job-analytics')

urlpatterns = [
    path('', include(router.urls)),
]
