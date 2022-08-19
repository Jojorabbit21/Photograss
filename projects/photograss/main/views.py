import os
import json
from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse
from django.templatetags.static import static
from .models import *

def index(request):
  path = settings.MEDIA_ROOT
  video = os.listdir(path + '/videos/')[0]
  context = {
    "video": video,
  }
  return render(request, 'main/splash.html', context)

def home(request):
  path = settings.MEDIA_ROOT
  img_list = MainCarousel.objects.all().values()
  context = {
    "images": img_list,
    }
  
  return render(request, 'main/home.html', context)

def snap(request):
  if request.method == 'POST':
    data = json.loads(request.body)
    context = {
      'result': data,
    }
    return JsonResponse(context)
  else:
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
  projects = PersonalProject.objects.all().values()
  project = get_object_or_404(PersonalProject, title=project_name)

  images = PersonalProject.objects.filter(title=project_name).prefetch_related('personal_project')[0]
  img = images.personal_project.all()
  request.project_path = str(request.path).replace("/projects/","")
  context = {
    'projects': projects,
    'project': project,
    'images': img,
  }
  return render(request, 'main/project_detail.html', context)

def commercial_main(request):
  projects = CommercialProject.objects.all().values()
  context = {
    "projects": projects,
  }
  return render(request, 'main/commercial.html', context)

def commercial_detail(request, project_name):
  projects = CommercialProject.objects.all().values()
  project = get_object_or_404(CommercialProject, title=project_name)
  
  images = CommercialProject.objects.filter(title=project_name).prefetch_related('commercial_project')[0]
  img = images.commercial_project.all()
  
  context = {
    'projects': projects,
    'project': project,
    'images': img,
  }
  return render(request, 'main/commercial_detail.html', context)