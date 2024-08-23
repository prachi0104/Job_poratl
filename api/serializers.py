from rest_framework import serializers
from .models import *




class JobApplicationSerializer(serializers.ModelSerializer):
    job_title = serializers.CharField(source='job.title', read_only=True)
    company = serializers.CharField(source='job.hr.username', read_only=True)

    class Meta:
        model = JobApplication
        fields = ['id', 'job', 'job_title','applier_name', 'company', 'applied_at','apply_to_email','resume',]


class PostSerializer(serializers.ModelSerializer):
    #applications = JobApplicationSerializer(many=True, read_only=True)
    #modified
    applications = serializers.SerializerMethodField()
    #
    class Meta:
        model = Post
        fields = '__all__'

     #MODIFIED
    def get_applications(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated and request.user.is_staff:
            applications = JobApplication.objects.filter(job=obj)
            return JobApplicationSerializer(applications, many=True).data
        return []





