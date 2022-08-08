from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Post(models.Model):
  title = models.CharField(max_length=200)
  desc = models.TextField(max_length=400, blank=False)
  user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
  
  def __str__(self):
    return self.title
  
class Photo(models.Model):
  post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True)
  image = models.ImageField(upload_to="img/", blank=True, null=True)