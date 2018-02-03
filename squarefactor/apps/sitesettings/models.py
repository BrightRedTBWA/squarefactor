from django.conf import settings
from django.contrib.sites.models import Site
from django.contrib.sites.managers import CurrentSiteManager
from django.core.cache import cache
from django.db import models

class SiteSetting(models.Model):
  browser_title = models.CharField(max_length=255, verbose_name='Default Browser Title')
  meta_keywords = models.TextField(blank=True, null=True, verbose_name='Default Meta Keywords')
  meta_description = models.TextField(blank=True, null=True, verbose_name='Default Meta Description')
  meta_additional = models.TextField(blank=True, null=True, verbose_name='Additional Meta Tags',
                                     help_text='Add additional meta tags (expires, generator, robots, author, etc) here.')
  analytics_code = models.TextField(blank=True, null=True, verbose_name='Analytics Code')
  site = models.ForeignKey(Site, unique=True)
  
  objects = models.Manager()
  current_site = CurrentSiteManager()
  
  class Meta:
    verbose_name_plural = verbose_name = 'Default Settings'
  
  def __unicode__(self):
    return '%s %s' % (self.site.domain, self.browser_title,)
  
  def save(self):
    super(SiteSetting, self).save()
    if hasattr(settings, 'SITE_NAME'):
      cache_key = 'site_settings_%s' % settings.SITE_NAME
    else:
      cache_key = 'site_settings'
    cache.delete(cache_key)

class AbstractSiteSetting(SiteSetting):
  class Meta:
    abstract = True
