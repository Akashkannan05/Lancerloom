from django.db import models
from django.contrib.auth.models import User
from datetime import date

# Create your models here.

class TechStackModel(models.Model):
    tech=models.CharField(max_length=50)
    category=models.CharField(max_length=30)

    def __str__(self):
        return f"{self.tech}-{self.category}"
    
class ProjectModel(models.Model):
    clientName=models.CharField(max_length=50)
    client=models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True)
    projectTitle=models.CharField(max_length=75)
    projectDesc=models.TextField()
    techStack=models.ManyToManyField(TechStackModel)
    features=models.TextField()
    budget=models.PositiveIntegerField(default=0)
    deadline=models.DateField()
    additionalNotes=models.TextField(null=True,blank=True)
    attachments=models.FileField(upload_to='attachments/',null=True,blank=True)
    duration=models.CharField(max_length=15,null=True,blank=True)
    inRefernce=models.BooleanField(default=False)
    completed=models.BooleanField(default=False)
    teamMembers=models.TextField(blank=True)
    formSubmissionDate=models.DateTimeField(auto_now=True)
    completedDate=models.DateField(null=True,blank=True)
    image = models.ImageField(upload_to='images/project/',null=True,blank=True) 

    
    def save(self, *args, **kwargs):
        if self.client is not None:
            self.clientName=self.client.username
        if self.deadline is not None:
            self.duration = (self.deadline - date.today()).days
        super().save(*args, **kwargs)
        
    def __str__(self):
        return f"{self.projectTitle}-{self.clientName}"