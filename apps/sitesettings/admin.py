from django.contrib import admin
from django.contrib.sites.models import Site

from squarefactor.apps.sitesettings.models import SiteSetting

class SiteSettingAdmin(admin.ModelAdmin):
  def formfield_for_dbfield(self, db_field, **kwargs):
    field = super(SiteSettingAdmin, self).formfield_for_dbfield(db_field, **kwargs)
    if db_field.name == 'site':
      field.widget.choices = [(s.id,s.domain) for s in Site.objects.order_by('domain')]
    return field

admin.site.register(SiteSetting, SiteSettingAdmin)
