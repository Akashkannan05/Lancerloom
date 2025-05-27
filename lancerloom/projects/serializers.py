from rest_framework import serializers
from .models import ProjectModel,TechStackModel

class TechStackSerializer(serializers.ModelSerializer):
    class Meta:
        model=TechStackModel
        fields=[
            'tech'
        ]

class ProjectSerializer(serializers.ModelSerializer):
    techStacks = TechStackSerializer(many=True)
    class Meta:
        model=ProjectModel
        fields=[
            'projectTitle',
            'projectDesc',
            'techStack',
            'duration'
        ]
