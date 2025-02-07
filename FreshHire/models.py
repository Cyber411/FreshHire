from django.db import models
from django.contrib.auth.models import User  # Use the default User model

class SeekerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE) # one to one relationship with the user model
    skills = models.TextField()
    education = models.CharField(max_length=255)
    resume = models.FileField(upload_to='resumes/',blank=True, null=True )
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)

    def __str__(self):
        return self.user.username


class EmployerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE) # one to one relationship with the user model
    company_name = models.CharField(max_length=255,blank=True, null=True)
    company_description = models.TextField()
    logo = models.ImageField(upload_to='logos/', blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)

    def __str__(self):
        return self.company_name


class Job(models.Model):
    employer = models.ForeignKey(EmployerProfile, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
    class Meta:
       ordering=['-created_at']


class Application(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    seeker = models.ForeignKey(SeekerProfile, on_delete=models.CASCADE)
    applied_at = models.DateTimeField(auto_now_add=True)
    cover_letter = models.TextField(null=True)
    status = models.CharField(max_length=50, default='Applied')

    def __str__(self):
        return f"{self.seeker.user.username} - {self.job.title}"
    
    class Meta:
       ordering=['-applied_at']




class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Message from {self.sender} to {self.recipient}"
