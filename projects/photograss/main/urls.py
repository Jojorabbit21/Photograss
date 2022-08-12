from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

app_name = 'main'

urlpatterns = [
  path('', views.index),
  path("home", views.home, name='home'),
  path("snap", views.snap, name="snap"),
  path("projects", views.project_main, name="project"),
  path("projects/<int:project_name", views.project_detail, name="project_detail"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)