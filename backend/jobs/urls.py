from django.urls import path, include
from rest_framework.routers import DefaultRouter
from jobs.views import (
    JobCategoryViewSet,
    JobViewSet,
    JobApplicationViewSet,
)

router = DefaultRouter()
router.register(r'categories', JobCategoryViewSet)
router.register(r'jobs', JobViewSet, basename='job')
router.register(r'applications', JobApplicationViewSet, basename='application')

urlpatterns = [
    path('', include(router.urls)),
    path('search/', JobViewSet.as_view({'get': 'search'}), name='job-search'),
    path('search/suggestions/', JobViewSet.as_view({'get': 'suggestions'}), name='search-suggestions'),
    path('search/popular/', JobViewSet.as_view({'get': 'popular'}), name='popular-searches'),
    path('search/location/', JobViewSet.as_view({'get': 'location'}), name='location-search'),
    path('jobs/<int:pk>/similar/', JobViewSet.as_view({'get': 'similar'}), name='similar-jobs'),
]
