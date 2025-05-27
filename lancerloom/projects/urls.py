from django.urls import path
from . import views

urlpatterns=[
    path('home/techStack/',views.TechStackClass),
    path('home/projectList/',views.ProjectHomeClass)
]