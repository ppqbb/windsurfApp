import django_filters
from django.db.models import Q
from .models import Job

class JobFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(method='filter_search')
    employment_type = django_filters.CharFilter(field_name='employment_type')  # Use employment_type instead of job_type
    experience_level = django_filters.CharFilter(field_name='experience_level')
    location = django_filters.CharFilter(field_name='location', lookup_expr='icontains')
    is_remote = django_filters.BooleanFilter(field_name='is_remote')
    salary_min = django_filters.NumberFilter(field_name='salary_min', lookup_expr='gte')
    salary_max = django_filters.NumberFilter(field_name='salary_max', lookup_expr='lte')
    category = django_filters.NumberFilter(field_name='category')

    def filter_search(self, queryset, name, value):
        if value:
            return queryset.filter(
                Q(title__icontains=value) |
                Q(description__icontains=value) |
                Q(requirements__icontains=value) |
                Q(responsibilities__icontains=value) |
                Q(skills_required__icontains=value)
            )
        return queryset

    class Meta:
        model = Job
        fields = [
            'search',
            'employment_type',
            'experience_level',
            'location',
            'is_remote',
            'salary_min',
            'salary_max',
            'category'
        ]
