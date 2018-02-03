from django.conf import settings
from django.core.cache import cache

from squarefactor.apps.sitesettings.models import SiteSetting

def site_settings(request):
  """
  You must make your own context_processor with a site_settings method if you subclass AbstractSiteSetting.
  It should use your child class of AbstractSiteSetting instead of SiteSetting as below
  """
  if hasattr(settings, 'SITE_NAME'):
    cache_key = 'site_settings_%s' % settings.SITE_NAME
  else:
    cache_key = 'site_settings_%s' % settings.SITE_ID
  site_settings = cache.get(cache_key)
  if site_settings is None:
    site_settings = SiteSetting.current_site.all()
    if site_settings:
      site_settings = site_settings[0]
      cache.set(cache_key, site_settings)
    else:
      return {
        'META_BROWSER_TITLE': '',
        'META_KEYWORDS': '',
        'META_DESCRIPTION': '',
        'META_ADDITIONAL': '',
        'ANALYTICS_CODE': ''
      }
  return {
    'META_BROWSER_TITLE': site_settings.browser_title,
    'META_KEYWORDS': site_settings.meta_keywords,
    'META_DESCRIPTION': site_settings.meta_description,
    'META_ADDITIONAL': site_settings.meta_additional,
    'ANALYTICS_CODE': site_settings.analytics_code
  }
