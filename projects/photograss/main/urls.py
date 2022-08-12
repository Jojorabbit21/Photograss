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
  path("projects/<str:project_name>", views.project_detail, name="project_detail"),
  path("commercial", views.commercial_main, name="commercial"),
  path("commercial/<str:project_name>", views.commercial_detail, name="commercial_detail"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)