import os
import shutil
from re import S
from functools import wraps
from tkinter import E
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from colorfield.fields import ColorField
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
  thumbnail = models.ImageField(upload_to="imgs/commercial", blank=True, null=True)
  desc = models.TextField(max_length=400, blank=False)
  user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
  
  class Meta:
    verbose_name = "Commercial Project"
    verbose_name_plural = "Commercial Project"
    
  def __str__(self):
    return self.title 
  
  @property
  def get_directory(self):
    return self._meta.get_field("title").value_from_object(self)
  
  @property
  def filename(self):
    return os.path.basename(self.thumbnail.name)
  
class CommercialPhotos(models.Model):
  post = models.ForeignKey(CommercialProject, on_delete=models.CASCADE, null=True, related_name='commercial_project')
  image = models.ImageField(upload_to="imgs/commercial", blank=True, null=True)
  
  class Meta:
    verbose_name = "Commercial Project Photos"
    verbose_name_plural = "Commercial Project Photo"
  
  @property
  def directory(self):
    return self.post.title
  
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
  thumbnail = models.ImageField(upload_to="imgs/project", blank=True, null=True)
  desc = models.TextField(max_length=400, blank=False)
  user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
  
  class Meta:
    verbose_name = "Personal Project"
    verbose_name_plural = "Personal Project"
    
  def __str__(self):
    return self.title
  
  def url(self):
    return str(self.title).replace(" ","_")
  
  @property
  def filename(self):
    return os.path.basename(self.thumbnail.name)
  
  @property
  def get_directory(self):
    return self._meta.get_field("title").value_from_object(self)
  
class PersonalPhotos(models.Model):
  post = models.ForeignKey(PersonalProject, on_delete=models.CASCADE, null=True, related_name="personal_project")
  image = models.ImageField(upload_to="imgs/project", blank=True, null=True)

  class Meta:
    verbose_name = "Personal Project Photos"
    verbose_name_plural = "Personal Project Photo"
  
  @property
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
  background_color = ColorField(default="#FFFFFF", format="hexa")
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
  attFile.video.delete(save=False)
  
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
  
@receiver(post_delete, sender=CommercialProject)
def deleteCommercialDir(sender, instance, **kwargs):
  title = instance.title
  if os.path.exists('./media/imgs/commercial/{}'.format(title)):
    shutil.rmtree('./media/imgs/commercial/{}'.format(title))
  
@receiver(post_delete, sender=CommercialPhotos)
def deleteAttFile(sender, **kwargs):
  attFile = kwargs.get("instance")
  attFile.image.delete(save=False)

@receiver(pre_save, sender=PersonalProject)
def createProjectDir(sender, instance, **kwargs):
  pr_dir = "./media/imgs/project/{}".format(instance.get_directory)
  if not os.path.exists(pr_dir):
    os.makedirs(pr_dir)
    
@receiver(post_save, sender=PersonalProject)
def movePersonalProjectPhoto(sender, instance, **kwagrs):
  if not instance:
    return
  if hasattr(instance, "_dirty"):
    return
  
  if os.path.isfile(f'./media/imgs/project/{instance.title}/{instance.filename}'):
    return
  else:
    instance.thumbnail = f'imgs/project/{instance.title}/{instance.filename}'
    shutil.move("./media/imgs/project/"+instance.filename, f'./media/imgs/project/{instance.get_directory}')
    try:
      instance._dirty = True
      instance.save()
    finally:
      del instance._dirty
  
@receiver(post_save, sender=PersonalPhotos)
def movePhotos(sender, instance, **kwargs):
  
  if not instance:
    return
  if hasattr(instance, "_dirty"):
    return
  
  dirname = instance.directory
  move_to = str(instance.image).replace('imgs/project/', '')
  instance.image = f'imgs/project/{dirname}/{move_to}'
  
  legacy_url = str(instance.image).replace(f'imgs/project/{dirname}','')
  shutil.move('./media/imgs/project'+legacy_url, f'./media/imgs/project/{dirname}/{legacy_url}')
  
  try:
    instance._dirty = True
    instance.save()
  finally:
    del instance._dirty
    
   
@receiver(pre_save, sender=CommercialProject)
def createCommercialDir(sender, instance, **kwargs):
  pr_dir = "./media/imgs/commercial/{}".format(instance.title)
  if not os.path.exists(pr_dir):
    os.makedirs(pr_dir)
    
@receiver(post_save, sender=CommercialProject)
def moveCommercialProjectPhoto(sender, instance, **kwargs):
  if not instance:
    return
  if hasattr(instance, "_dirty"):
    return
  
  if os.path.isfile(f'./media/imgs/commercial/{instance.title}/{instance.filename}'):
    return
  else:
    instance.thumbnail = f'imgs/commercial/{instance.title}/{instance.filename}'
    shutil.move("./media/imgs/commercial/"+instance.filename, f'./media/imgs/commercial/{instance.get_directory}')
    
    try:
      instance._dirty = True
      instance.save()
    finally:
      del instance._dirty

@receiver(post_save, sender=CommercialPhotos)
def moveCommercialPhotos(sender, instance, **kwargs):
  
  if not instance:
    return
  if hasattr(instance, '_dirty'):
    return
  
  dirname = instance.directory()
  move_to = str(instance.image).replace('imgs/commercial/', '')
  instance.image = f'imgs/commercial/{dirname}/{move_to}'
  
  legacy_url = str(instance.image).replace(f'imgs/commercial/{dirname}', '')
  shutil.move('./media/imgs/commercial'+legacy_url, f'./media/imgs/commercial/{dirname}/{legacy_url}')
  
  try:
    instance._dirty = True
    instance.save()
  finally:
    del instance._dirty
  
  
  

