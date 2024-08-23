from django.shortcuts import render
from django.core.exceptions import PermissionDenied
from rest_framework import viewsets,permissions
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from .permissions import *
from .models import *
from .serializers import *

# Create your views here.

class PostViewSet(viewsets.ModelViewSet):
    queryset=Post.objects.all()
    serializer_class=PostSerializer
    authentication_classes=[SessionAuthentication]
    permission_classes=[IsStaffOrReadOnly]
    filter_backends=[SearchFilter]
    search_fields=['hr__username','title','location']

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            if user.is_staff:
                # If the user is an HR, show only their posts
                return Post.objects.filter(hr=user)
            else:
                # If the user is not an HR, show posts created by HRs
        
             return Post.objects.filter(hr__is_staff=True)
        #modified
        return Post.objects.all()  # Show HR posts to unauthenticated users

    def perform_create(self, serializer):
        if not self.request.user.is_staff:
            raise PermissionDenied("Only HRs can create posts.")
        serializer.save(hr=self.request.user)

    def perform_update(self, serializer):
        # Allow only HRs to update posts
        if not self.request.user.is_staff:
            raise PermissionDenied("You do not have permission to edit this post.")
        serializer.save(hr=self.request.user)

    def perform_destroy(self, instance):
        # Allow only HRs to delete posts
        if not self.request.user.is_staff:
            raise PermissionDenied("You do not have permission to delete this post.")
        instance.delete()

  #MODIFIED
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context



class ApplyViewSet(viewsets.ModelViewSet):
    queryset = JobApplication.objects.all()
    serializer_class = JobApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            if user.is_staff:
                return JobApplication.objects.filter(job__hr=user)
            else:
                return JobApplication.objects.filter(applier_name=user.username, job__hr__is_staff=True)
        return JobApplication.objects.none()

    def perform_create(self, serializer):
        job = Post.objects.get(id=self.request.data['job'])
        #modified
        if not self.request.user.is_staff and not job.hr.is_staff:
            raise PermissionDenied("You can only apply to jobs posted by HRs.")
        serializer.save(user=self.request.user, job=job,apply_to_email=job.apply_to_email)


"""   def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return Post.objects.filter(hr=user)
        return Post.objects.all()  # Or Post.objects.all() if you want to show all posts to unauthenticated users

    def perform_create(self, serializer):
        serializer.save(hr=self.request.user) """


