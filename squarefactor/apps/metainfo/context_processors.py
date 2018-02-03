from django.conf import settings
from django.core.cache import cache

from squarefactor.apps.metainfo.models import MetaInformation
from squarefactor.apps.sitesettings.context_processors import site_settings

def meta_settings(request):
  _site_settings = site_settings(request)
  if hasattr(settings, 'SITE_NAME'):
    cache_key = 'metainfo_%s_%s' % (request.path, settings.SITE_NAME)
  else:
    cache_key = 'metainfo_%s'  % request.path
  meta_info = cache.get(cache_key)
  if meta_info is None:
    try:
      meta_info = MetaInformation.objects.get(url=request.path)
    except MetaInformation.DoesNotExist:
      return _site_settings
  cache.set(cache_key, meta_info)
  return {'META_BROWSER_TITLE': meta_info.browser_title,
          'META_KEYWORDS': meta_info.meta_keywords,
          'META_DESCRIPTION': meta_info.meta_description,
          'META_ADDITIONAL': meta_info.meta_additional,
          'ANALYTICS_CODE': _site_settings['ANALYTICS_CODE']
         }
