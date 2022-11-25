from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

app_name = 'main'

urlpatterns = [
  # path('', views.index),
  path("", views.home, name='home'),
  path("snaps", views.snap, name="snap"),
  path("projects", views.project_main, name="project"),
  path("projects/<int:project_id>", views.project_detail, name="project_detail"),
  path("commercial", views.commercial_main, name="commercial"),
  path("commercial/<int:project_id>", views.commercial_detail, name="commercial_detail"),
  path("about/", views.about, name="about"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)