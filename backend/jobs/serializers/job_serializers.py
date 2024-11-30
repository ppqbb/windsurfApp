from rest_framework import serializers
from jobs.models import (
    JobCategory, Job, JobApplication,
    CustomApplicationQuestion, ApplicationAnswer
)
from accounts.serializers.user_serializers import UserSerializer, CompanyProfileSerializer

class JobCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = JobCategory
        fields = ('id', 'name', 'description')

class CustomApplicationQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomApplicationQuestion
        fields = ('id', 'question_type', 'question_text', 'choices', 'is_required')

class JobSerializer(serializers.ModelSerializer):
    company = CompanyProfileSerializer(read_only=True)
    category = JobCategorySerializer(read_only=True)
    custom_questions = CustomApplicationQuestionSerializer(many=True, read_only=True)
    
    class Meta:
        model = Job
        fields = ('id', 'company', 'title', 'description', 'requirements',
                 'category', 'job_type', 'experience_level', 'location',
                 'salary_range', 'status', 'created_at', 'updated_at',
                 'deadline', 'custom_questions')
        read_only_fields = ('id', 'created_at', 'updated_at')

class JobListSerializer(serializers.ModelSerializer):
    company_name = serializers.CharField(source='company.company_name')
    category_name = serializers.CharField(source='category.name')
    
    class Meta:
        model = Job
        fields = ('id', 'title', 'company_name', 'category_name', 'location',
                 'job_type', 'experience_level', 'created_at', 'deadline')

class ApplicationAnswerSerializer(serializers.ModelSerializer):
    question_text = serializers.CharField(source='question.question_text', read_only=True)
    
    class Meta:
        model = ApplicationAnswer
        fields = ('id', 'question', 'question_text', 'answer')

class JobApplicationSerializer(serializers.ModelSerializer):
    applicant = UserSerializer(read_only=True)
    job = JobSerializer(read_only=True)
    answers = ApplicationAnswerSerializer(many=True, read_only=True)
    
    class Meta:
        model = JobApplication
        fields = ('id', 'job', 'applicant', 'cover_letter', 'resume',
                 'status', 'applied_at', 'updated_at', 'answers')
        read_only_fields = ('id', 'applied_at', 'updated_at')

class JobApplicationCreateSerializer(serializers.ModelSerializer):
    answers = ApplicationAnswerSerializer(many=True)
    
    class Meta:
        model = JobApplication
        fields = ('job', 'cover_letter', 'resume', 'answers')

    def create(self, validated_data):
        answers_data = validated_data.pop('answers')
        application = JobApplication.objects.create(**validated_data)
        
        for answer_data in answers_data:
            ApplicationAnswer.objects.create(application=application, **answer_data)
        
        return application
