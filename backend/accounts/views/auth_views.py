from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from accounts.serializers import (
    UserSerializer,
    UserRegistrationSerializer,
    ApplicantProfileSerializer,
    CompanyProfileSerializer,
)
from accounts.models import ApplicantProfile, CompanyProfile

User = get_user_model()

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'create':
            return UserRegistrationSerializer
        return self.serializer_class

    @action(detail=False, methods=['get'])
    def me(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def register(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            
            # Create corresponding profile based on user type
            if user.user_type == 'applicant':
                ApplicantProfile.objects.create(user=user)
            elif user.user_type == 'company':
                CompanyProfile.objects.create(user=user)
            
            return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ApplicantProfileViewSet(viewsets.ModelViewSet):
    serializer_class = ApplicantProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.user_type == 'admin':
            return ApplicantProfile.objects.all()
        return ApplicantProfile.objects.filter(user=self.request.user)

class CompanyProfileViewSet(viewsets.ModelViewSet):
    serializer_class = CompanyProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.user_type == 'admin':
            return CompanyProfile.objects.all()
        return CompanyProfile.objects.filter(user=self.request.user)
