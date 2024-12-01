from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from .serializers import UserSerializer, RegisterSerializer, CompanyProfileSerializer, ApplicantProfileSerializer
from .models import ApplicantProfile, CompanyProfile
from jobs.permissions import IsAdmin

User = get_user_model()

class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:
            user = User.objects.get(email=request.data['email'])
            response.data['user'] = UserSerializer(user).data
        return response

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.action == 'create':
            return [AllowAny()]
        return super().get_permissions()

    def create(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get', 'put', 'patch'])
    def me(self, request):
        user = request.user
        if request.method == 'GET':
            serializer = self.get_serializer(user)
            return Response(serializer.data)
        
        serializer = self.get_serializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ApplicantProfileViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return User.objects.filter(user_type='applicant')

class CompanyProfileViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return User.objects.filter(user_type='company')

class CompanyViewSet(viewsets.ModelViewSet):
    queryset = CompanyProfile.objects.all()
    serializer_class = CompanyProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.action in ['create', 'update_subscription']:
            return [IsAuthenticated(), IsAdmin()]
        if self.action in ['update', 'partial_update']:
            return [IsAuthenticated()]
        return [IsAuthenticated()]

    def get_queryset(self):
        if self.request.user.user_type == 'admin':
            return CompanyProfile.objects.all()
        elif self.request.user.user_type == 'company':
            return CompanyProfile.objects.filter(user=self.request.user)
        return CompanyProfile.objects.none()

    @action(detail=True, methods=['post'])
    def update_subscription(self, request, pk=None):
        company = self.get_object()
        subscription_type = request.data.get('subscription_type')
        
        if subscription_type not in ['standard', 'premium']:
            return Response(
                {'detail': 'Invalid subscription type'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        company.subscription_type = subscription_type
        company.save()
        return Response({'status': 'subscription updated'})

class ApplicantViewSet(viewsets.ModelViewSet):
    serializer_class = ApplicantProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.user_type == 'admin':
            return ApplicantProfile.objects.all()
        elif self.request.user.user_type == 'applicant':
            return ApplicantProfile.objects.filter(user=self.request.user)
        elif self.request.user.user_type == 'company' and self.request.user.company_profile.subscription_type == 'premium':
            return ApplicantProfile.objects.filter(
                applications__job__company=self.request.user.company_profile
            ).distinct()
        return ApplicantProfile.objects.none()
