from django.conf import settings
from django.core.cache import cache
from django.db import models

class MetaInformation(models.Model):
  url = models.CharField(max_length=255, unique=True, 
      help_text='Enter a valid url with leading and trailing slashes. e.g. /products/ or /contact/')
  browser_title = models.CharField(max_length=255, blank=True)
  meta_keywords = models.TextField(blank=True, null=True)
  meta_description = models.TextField(blank=True, null=True)
  meta_additional = models.TextField(blank=True, null=True, verbose_name='Additional Meta Tags',
                                     help_text='Add additional meta tags (expires, generator, robots, author, etc) here.')
  
  class Meta:
    """ Oh the irony... """
    verbose_name_plural = verbose_name = 'Meta Tags'
  
  def __unicode__(self):
    return self.url
  
  def save(self):
    super(MetaInformation, self).save()
    if hasattr(settings, 'SITE_NAME'):
      cache_key = 'metainfo_%s_%s' % (self.url, settings.SITE_NAME)
    else:
      cache_key = 'metainfo_%s' % self.url
    cache.delete(cache_key)
