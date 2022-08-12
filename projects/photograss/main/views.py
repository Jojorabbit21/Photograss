import os
from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.templatetags.static import static
from .models import *

def index(request):
  return render(request, 'main/splash.html')

def home(request):
  path = settings.MEDIA_ROOT
  img_list = os.listdir(path + '/imgs/main_carousel/')
  context = {
    "images": img_list,
    "prefix": settings.MEDIA_URL,
    }
  
  return render(request, 'main/home.html', context)

def snap(request):
  path = settings.MEDIA_ROOT
  img_list = os.listdir(path + '/imgs/snap/')
  context = {
    "images": img_list,
    "prefix": settings.MEDIA_URL,
    }
  return render(request, 'main/snap.html', context)

def project_main(request):
  projects = PersonalProject.objects.all().values()
  context = {
    "projects": projects,
  }
  return render(request, 'main/project.html', context)

def project_detail(request, project_name):
  project = get_object_or_404(PersonalProject)
  context = {
    'project': project,
  }
  return render(request, 'main/project_detail.html', context)