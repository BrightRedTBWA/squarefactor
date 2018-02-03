from django.conf import settings
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext

from squarefactor.apps.formbuilder.forms import BuiltForm

def formbuilder(request, url):
  if not url.endswith('/') and settings.APPEND_SLASH:
    return HttpResponseRedirect("%s/" % request.path)
  if not url.startswith('/'):
    url = "/" + url
  
  show_sfformbuilder_confirmation = False
  if request.method == 'POST':
    f = BuiltForm(request.POST, url=url)
    if f.is_valid():
      f.save()
      return HttpResponseRedirect(f.instance.url + '?_sfform_submitted=1')
  else:
    f = BuiltForm(url=request.path)
    if '_sfform_submitted' in request.GET:
      show_sfformbuilder_confirmation = True
  if f.instance.template:
    template = f.instance.template
  else:
    template = 'formbuilder_default.html'
  return render_to_response(template, locals(), context_instance=RequestContext(request))