from django.shortcuts import render
from django.contrib.auth.models import User

# Create your views here.
from rest_framework.exceptions import ValidationError,NotFound
from rest_framework.response import Response
from rest_framework import generics,views
from rest_framework import status
from rest_framework import permissions,authentication

from .models import TechStackModel,ProjectModel
from .serializers import TechStackSerializer,ProjectSerializer

class TechStackView(generics.ListAPIView):
    queryset=TechStackModel.objects.all()
    serializer_class=TechStackSerializer
    permission_classes=[permissions.AllowAny]
    
    def get(self, request, *args, **kwargs):
        List=[]
        for techStack in self.get_queryset():
            List.append(techStack.tech)
        return Response({"techStack":List})
    
TechStackClass=TechStackView.as_view()

class ProjectHomeView(generics.ListAPIView):
    queryset=ProjectModel.objects.all()
    serializer_class=ProjectSerializer
    permission_classes=permissions.AllowAny

    def get_queryset(self):
        projects=ProjectModel.objects.filter(completed=True).order_by("-completedDate")
        if not projects.exists():
            raise ValidationError("Currently there is no project")
        return projects[:6]
ProjectHomeClass=ProjectHomeView.as_view()