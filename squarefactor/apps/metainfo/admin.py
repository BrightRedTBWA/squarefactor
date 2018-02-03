from django.contrib import admin
from squarefactor.apps.metainfo.models import MetaInformation

class MetaInformationAdmin(admin.ModelAdmin):
  ordering = ['url']
  search_fields = ['url','meta_keyworkds','meta_description']
  
admin.site.register(MetaInformation, MetaInformationAdmin)
