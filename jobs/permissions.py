from rest_framework import permissions

class IsCompanyOrAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.user_type in ['company', 'admin']

    def has_object_permission(self, request, view, obj):
        if request.user.user_type == 'admin':
            return True
        return obj.company.user == request.user

class IsCompanyWithinJobLimit(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method != 'POST' or request.user.user_type != 'company':
            return True
            
        company_profile = request.user.company_profile
        active_jobs_count = company_profile.jobs.filter(status__in=['active', 'pending']).count()
        
        if company_profile.subscription_type == 'standard' and active_jobs_count >= 5:
            return False
        return True

class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.user_type == 'admin'

class IsApplicant(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.user_type == 'applicant'

    def has_object_permission(self, request, view, obj):
        return obj.applicant == request.user
