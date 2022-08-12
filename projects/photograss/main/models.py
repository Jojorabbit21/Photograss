import os
import shutil
from re import S
import string
import random
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
# Deleting Files from admin
from django.db.models.signals import post_delete, pre_save, post_save
from django.dispatch import receiver
# Random String
from django.utils.crypto import get_random_string

def generate_id():
  return get_random_string(7)

# Commercials
class CommercialProject(models.Model):
  title = models.CharField(max_length=200)
  client = models.CharField(max_length=200)
  desc = models.TextField(max_length=400, blank=False)
  user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
  
  class Meta:
    verbose_name = "Commercial Project"
    verbose_name_plural = "Commercial Project"
    
  def __str__(self):
    return self.title + " / client : " + self.client  
  
  def get_directory(self):
    return self._meta.get_field("title").value_from_object(self) + "_" + self._meta.get_field("client").value_from_object(self)
  
class CommercialPhotos(models.Model):
  post = models.ForeignKey(CommercialProject, on_delete=models.CASCADE, null=True)
  image = models.ImageField(upload_to="imgs/commercial", blank=True, null=True)
  
  class Meta:
    verbose_name = "Commercial Project Photos"
    verbose_name_plural = "Commercial Project Photo"
  
  def directory(self):
    return self.post.title + "_" + self.post.client
  
# Snap Photos
class Snapshot(models.Model):

  title = models.CharField(max_length=200, default=generate_id)
  image = models.ImageField(upload_to="imgs/snap/", blank=True, null=True)
  
  class Meta:
    verbose_name = "Snapshot"
    verbose_name_plural = "Snapshot"
    
  def __str__(self):
    return self.title  

  
# Personal Projects
class PersonalProject(models.Model):
  title = models.CharField(max_length=200)
  serial = models.CharField(max_length=50, default=generate_id)
  desc = models.TextField(max_length=400, blank=False)
  user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
  
  class Meta:
    verbose_name = "Personal Project"
    verbose_name_plural = "Personal Project"
    
  def __str__(self):
    return self.title
  
  def get_directory(self):
    return self._meta.get_field("title").value_from_object(self)
  
class PersonalPhotos(models.Model):
  post = models.ForeignKey(PersonalProject, on_delete=models.CASCADE, null=True)
  image = models.ImageField(upload_to="imgs/project", blank=True, null=True)

  class Meta:
    verbose_name = "Personal Project Photos"
    verbose_name_plural = "Personal Project Photo"
    
  def directory(self):
    return self.post.title
    

# Index Video
class MainVideo(models.Model):
  desc = models.CharField(max_length=200, default="MainVideo", blank=False)
  video = models.FileField(upload_to="videos/", null=True, verbose_name="")
  
  class Meta:
    verbose_name = "Main Video"
    verbose_name_plural = "Main Video"
  
  def __str__(self):
    return self.desc + ":" + str(self.video)

# Main Page Carousel Slides
class MainCarousel(models.Model):
  desc = models.CharField(max_length=200, blank=False)
  image = models.ImageField(upload_to="imgs/main_carousel/", blank=True, null=True)
  
  class Meta:
    verbose_name = "Carousel"
    verbose_name_plural = "Carousel"
    
  def __str__(self):
    return self.desc

@receiver(post_delete, sender=MainCarousel)
def deleteAttFile(sender, **kwargs):
  attFile = kwargs.get("instance")
  attFile.image.delete(save=False)

@receiver(post_delete, sender=MainVideo)
def deleteAttFile(sender, **kwargs):
  attFile = kwargs.get("instance")
  attFile.image.delete(save=False)
  
@receiver(post_delete, sender=Snapshot)
def deleteAttFile(sender, **kwargs):
  attFile = kwargs.get("instance")
  attFile.image.delete(save=False)
  
@receiver(post_delete, sender=PersonalProject)
def deleteProjectDir(sender, instance, **kwargs):
  title = instance.title
  if os.path.exists("./media/imgs/project/{}".format(title)):
    shutil.rmtree("./media/imgs/project/{}".format(title))
    
@receiver(post_delete, sender=PersonalPhotos)
def deleteAttFile(sender, **kwargs):
  attFile = kwargs.get("instance")
  attFile.image.delete(save=False)
  
@receiver(post_delete, sender=CommercialPhotos)
def deleteAttFile(sender, **kwargs):
  attFile = kwargs.get("instance")
  attFile.image.delete(save=False)

@receiver(pre_save, sender=PersonalProject)
def createProjectDir(sender, instance, **kwargs):
  pr_dir = "./media/imgs/project/{}".format(instance.get_directory())
  if not os.path.exists(pr_dir):
    os.makedirs(pr_dir)
    
@receiver(post_save, sender=PersonalPhotos)
def movePhotos(sender, instance, **kwargs):
  dirname = instance.directory()
  move_to = str(instance.image).replace('imgs/project/', '')
  shutil.move('./media/'+str(instance.image), f'./media/imgs/project/{dirname}/{move_to}')
  
@receiver(pre_save, sender=CommercialProject)
def createCommercialDir(sender, instance, **kwargs):
  pr_dir = "./media/imgs/commercial/{}".format(instance.get_directory())
  if not os.path.exists(pr_dir):
    os.makedirs(pr_dir)
    
@receiver(post_save, sender=CommercialPhotos)
def moveCommercialPhotos(sender, instance, **kwargs):
  dirname = instance.directory()
  move_to = str(instance.image).replace('imgs/commercial/', '')
  shutil.move('./media/'+str(instance.image), f'./media/imgs/commercial/{dirname}/{move_to}')