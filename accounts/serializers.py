from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import ApplicantProfile, CompanyProfile

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'user_type', 'first_name', 'last_name', 'phone_number', 'profile_picture')
        read_only_fields = ('id', 'email', 'user_type')

class CompanyProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = CompanyProfile
        fields = ('id', 'user', 'company_name', 'description', 'website', 
                 'industry', 'company_size', 'founded_year', 'logo', 
                 'subscription_type')

class ApplicantProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = ApplicantProfile
        fields = ('id', 'user', 'resume', 'skills', 'experience', 
                 'education', 'preferred_job_categories', 'preferred_locations')

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('email', 'username', 'password', 'confirm_password', 'user_type', 'first_name', 'last_name')

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("Passwords do not match.")
        if len(data['password']) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters long.")
        return data

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        user = User.objects.create_user(**validated_data)
        
        if user.user_type == 'applicant':
            ApplicantProfile.objects.create(user=user)
        elif user.user_type == 'company':
            CompanyProfile.objects.create(user=user)
            
        return user
