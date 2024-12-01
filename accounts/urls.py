from django.urls import path, include
from rest_framework.routers import DefaultRouter
from accounts.views import (
    UserViewSet,
    ApplicantProfileViewSet,
    CompanyProfileViewSet,
)

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'applicant-profiles', ApplicantProfileViewSet, basename='applicant-profile')
router.register(r'company-profiles', CompanyProfileViewSet, basename='company-profile')

urlpatterns = [
    path('', include(router.urls)),
]
