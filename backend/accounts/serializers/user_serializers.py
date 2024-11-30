from rest_framework import serializers
from django.contrib.auth import get_user_model
from accounts.models import ApplicantProfile, CompanyProfile

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'user_type', 'phone_number', 'profile_picture')
        read_only_fields = ('id',)

class ApplicantProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = ApplicantProfile
        fields = ('id', 'user', 'resume', 'skills', 'experience', 'education',
                 'preferred_job_categories', 'preferred_locations')
        read_only_fields = ('id',)

    def update(self, instance, validated_data):
        # Remove user data from validated_data if present
        validated_data.pop('user', None)
        return super().update(instance, validated_data)

class CompanyProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = CompanyProfile
        fields = ('id', 'user', 'company_name', 'description', 'website',
                 'industry', 'company_size', 'founded_year', 'logo',
                 'subscription_type')
        read_only_fields = ('id',)

    def update(self, instance, validated_data):
        # Remove user data from validated_data if present
        validated_data.pop('user', None)
        return super().update(instance, validated_data)

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('email', 'username', 'password', 'confirm_password',
                 'user_type', 'phone_number')

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("Passwords do not match.")
        return data

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        password = validated_data.pop('password')
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user
