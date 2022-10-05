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

# Personal Projects
class PersonalProject(models.Model):
  title = models.CharField(max_length=200)
  serial = models.CharField(max_length=50, default=generate_id)
  thumbnail = models.ImageField(upload_to="imgs/project", blank=True, null=True)
  desc = models.TextField(max_length=400, blank=False)
  user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)

  class Meta:
    verbose_name = "Personal Project"
    verbose_name_plural = "Personal Projects"
    
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
  post = models.ForeignKey(PersonalProject, on_delete=models.CASCADE, null=True)
  image = models.ImageField(upload_to="imgs/project", blank=True, null=True)
  
  class Meta:
    verbose_name = "Personal Project Photos"
    verbose_name_plural = "Personal Project Photos"
  
  @property
  def directory(self):
    return self.post.title
  
@receiver(post_save, sender=PersonalProject)
def movePersonalProjectPhoto(sender, instance, **kwagrs):
  pr_dir = "./media/imgs/project/{}".format(instance.id)
  if not os.path.exists(pr_dir):
    os.makedirs(pr_dir)
  try:
    shutil.move("./media/imgs/project/"+instance.filename, f'./media/imgs/project/{instance.id}')
  except:
    pass
  PersonalProject.objects.filter(id=instance.id).update(thumbnail=f'imgs/project/{instance.id}/{instance.filename}')

@receiver(post_save, sender=PersonalPhotos)
def movePhotos(sender, instance, **kwargs):
  dirname = instance.post.id
  filename = str(instance.image).replace('imgs/project/', '')
  try:
    shutil.move(f'./media/imgs/project/{filename}', f'./media/imgs/project/{dirname}/{filename}')
  except:
    pass
  PersonalPhotos.objects.filter(id=instance.id).update(image=f'imgs/project/{dirname}/{filename}')
    
@receiver(post_delete, sender=PersonalProject)
def deleteProjectDir(sender, instance, **kwargs):
  id = instance.id
  if os.path.exists("./media/imgs/project/{}".format(id)):
    shutil.rmtree("./media/imgs/project/{}".format(id))
    
@receiver(post_delete, sender=PersonalPhotos)
def deleteAttFile(sender, **kwargs):
  attFile = kwargs.get("instance")
  attFile.image.delete(save=False)
  
  
  
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
  post = models.ForeignKey(CommercialProject, on_delete=models.CASCADE, null=True)
  image = models.ImageField(upload_to="imgs/commercial", blank=True, null=True)

  class Meta:
    verbose_name = "Commercial Project Photos"
    verbose_name_plural = "Commercial Project Photo"
  
  @property
  def directory(self):
    return self.post.title

@receiver(post_save, sender=CommercialProject)
def moveCommercialProjectPhoto(sender, instance, **kwargs):
  pr_dir = "./media/imgs/commercial/{}".format(instance.id)
  if not os.path.exists(pr_dir):
    os.makedirs(pr_dir)
  try:
    shutil.move("./media/imgs/commercial/"+instance.filename, f'./media/imgs/commercial/{instance.id}')
  except:
    pass
  CommercialProject.objects.filter(id=instance.id).update(thumbnail=f'imgs/commercial/{instance.title}/{instance.filename}' )

@receiver(post_save, sender=CommercialPhotos)
def moveCommercialPhotos(sender, instance, **kwargs):
  dirname = instance.post.id
  filename = str(instance.image).replace('imgs/commercial/', '')
  try:
    shutil.move(f'./media/imgs/commercial/{filename}', f'./media/imgs/commercial/{dirname}/{filename}')
  except:
    pass
  CommercialPhotos.objects.filter(id=instance.id).update(image=f'imgs/commercial/{dirname}/{filename}')
  
@receiver(post_delete, sender=CommercialProject)
def deleteCommercialDir(sender, instance, **kwargs):
  id = instance.id
  if os.path.exists('./media/imgs/commercial/{}'.format(id)):
    shutil.rmtree('./media/imgs/commercial/{}'.format(id))  
    
@receiver(post_delete, sender=CommercialPhotos)
def deleteAttFile(sender, **kwargs):
  attFile = kwargs.get("instance")
  attFile.image.delete(save=False)
  
  
  

# Snap Photos
class Snapshot(models.Model):

  title = models.CharField(max_length=200, default=generate_id)
  image = models.ImageField(upload_to="imgs/snap/", blank=True, null=True)
  
  class Meta:
    verbose_name = "Snapshot"
    verbose_name_plural = "Snapshot"
    
  def __str__(self):
    return self.title  

@receiver(post_delete, sender=Snapshot)
def deleteAttFile(sender, **kwargs):
  attFile = kwargs.get("instance")
  attFile.image.delete(save=False)
  
  
  
# Index Video
class MainVideo(models.Model):
  desc = models.CharField(max_length=200, default="MainVideo", blank=False)
  video = models.FileField(upload_to="videos/", null=True, verbose_name="")
  
  class Meta:
    verbose_name = "Main Video"
    verbose_name_plural = "Main Video"
  
  def __str__(self):
    return self.desc + ":" + str(self.video)

@receiver(post_delete, sender=MainVideo)
def deleteAttFile(sender, **kwargs):
  attFile = kwargs.get("instance")
  attFile.video.delete(save=False)
  
  

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

  
  
  

