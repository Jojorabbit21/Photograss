from django.contrib import admin
from .models import *

# Personal Projects
class PersonalProjectInline(admin.TabularInline):
  model = PersonalPhotos
  
class PersonalProjectAdmin(admin.ModelAdmin):
  inlines = [PersonalProjectInline, ]
  
# Commercial
class CommercialInline(admin.TabularInline):
  model = CommercialPhotos

class CommercialAdmin(admin.ModelAdmin):
  inlines = [CommercialInline, ]

# Register your models here.
admin.site.register(MainVideo)
admin.site.register(MainCarousel)
admin.site.register(Snapshot)
admin.site.register(PersonalProject, PersonalProjectAdmin)
admin.site.register(CommercialProject, CommercialAdmin)