from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    hr = models.ForeignKey(User, on_delete=models.CASCADE)
    location=models.CharField(max_length=50,default="Vadodara")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    apply_to_email=models.EmailField(max_length=254,default="company@gmail.com")

    def __str__(self):
        return self.title
    

class JobApplication(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    applier_name=models.CharField(max_length=50,default="hemang")
    job = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="applications")
    apply_to_email = models.EmailField(max_length=254,default="company@gmail.com")
    resume = models.FileField(upload_to='resumes/', blank=True)
    applied_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} applied to {self.job.title}"
