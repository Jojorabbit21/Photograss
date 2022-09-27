import os
import json
from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse
from django.templatetags.static import static
from .models import *

domain = settings.DOMAIN

def index(request):
  path = settings.MEDIA_ROOT
  video = os.listdir(path + '/videos/')[0]
  context = {
    "domain": domain,
    "video": video,
  }
  return render(request, 'main/splash.html', context)

def home(request):
  img_list = MainCarousel.objects.all().values()
  context = {
    "domain": domain,
    "images": img_list,
    }
  return render(request, 'main/home.html', context)

def snap(request):
  if request.method == 'POST':
    data = json.loads(request.body)
    context = {
      'domain': domain,
      'result': data,
    }
    return JsonResponse(context)
  else:
    path = settings.MEDIA_ROOT
    img_list = os.listdir(path + '/imgs/snap/')
    context = {
      "domain": domain,
      "images": img_list,
      "prefix": settings.MEDIA_URL,
      }
    return render(request, 'main/snap.html', context)

def project_main(request):
  projects = PersonalProject.objects.all().values()
  context = {
    "domain": domain,
    "projects": projects,
  }
  return render(request, 'main/project.html', context)

def project_detail(request, project_id):
  projects = PersonalProject.objects.all().values()
  project = get_object_or_404(PersonalProject, pk=project_id)
  try:
    project_next = PersonalProject.objects.get(pk=(project_id + 1))
  except:
    project_next = None
  try:
    project_prev = PersonalProject.objects.get(pk=(project_id - 1))
  except:
    project_prev = None

  images = PersonalProject.objects.filter(pk=project_id).prefetch_related('personal_project')[0]
  img = images.personal_project.all()
  request.project_path = str(request.path).replace("/projects/","")
  context = {
    'domain': domain,
    'projects': projects,
    'project': project,
    'project_prev': project_prev,
    'project_next': project_next,
    'images': img,
  }
  return render(request, 'main/project_detail.html', context)

def commercial_main(request):
  projects = CommercialProject.objects.all().values()
  context = {
    "domain": domain,
    "projects": projects,
  }
  return render(request, 'main/commercial.html', context)

def commercial_detail(request, project_id):
  projects = CommercialProject.objects.all().values()
  project = get_object_or_404(CommercialProject, pk=project_id)  
  try:
    project_next = PersonalProject.objects.get(pk=(project_id + 1))
  except:
    project_next = None
  try:
    project_prev = PersonalProject.objects.get(pk=(project_id - 1))
  except:
    project_prev = None
  
  images = CommercialProject.objects.filter(pk=project_id).prefetch_related('commercial_project')[0]
  img = images.commercial_project.all()
  
  context = {
    'domain': domain,
    'projects': projects,
    'project': project,
    'project_prev': project_prev,
    'project_next': project_next,
    'images': img,
  }
  return render(request, 'main/commercial_detail.html', context)