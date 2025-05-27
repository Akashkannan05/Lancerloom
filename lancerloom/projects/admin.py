from django.contrib import admin

# Register your models here.
from .models import ProjectModel,TechStackModel

admin.site.register(ProjectModel)
admin.site.register(TechStackModel)