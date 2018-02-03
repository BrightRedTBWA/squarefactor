from django.conf import settings
from django.contrib.admin.widgets import AdminTextareaWidget
from django.forms.util import flatatt
from django.forms.widgets import FileInput, Select
from django.template.loader import render_to_string
from django.utils.encoding import force_unicode
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext as _

from squarefactor.utils.templatetags.thumbnail import thumbnail

class MarkdownWidget(AdminTextareaWidget):
  """ """

  def render(self, name, value, attrs=None):
    return render_to_string("markdown.html", locals())


class VideoEmbedTextarea(AdminTextareaWidget):
  """ shows a preview of the embedded video """
  def render(self, name, value, attrs=None):
    if value is None:
      value = ''
      spacer = ''
    else:
      value = force_unicode(value)
      spacer = ' '
    final_attrs = self.build_attrs(attrs, name=name)
    return mark_safe(u'<textarea%s>%s</textarea>%s%s' % (flatatt(final_attrs), conditional_escape(force_unicode(value)), spacer, value,))

class ImageFileInput(FileInput):
  """ shows a preview of the image instead of just a link to the image """
  def render(self, name, value, attrs=None):
    output = []
    rendered = super(ImageFileInput, self).render(name, value, attrs)
    if value and hasattr(value, "url"):
      url = thumbnail(value, "400")
      output.append('%s %s<br />%s <img src="%s" />' % (_('Change:'), rendered, _('Currently:'), url))
    else:
      output.append('%s %s' % (_('Upload:'), rendered,))
    return mark_safe(u''.join(output))

class WYSIWYGTextAreaWidget(AdminTextareaWidget):
  """ 
    Special textarea that gets converted into a TinyMCE WYSIWYG 

    To use this field add squarefactor.admin to your installed apps 
    then import the field into your model and use it like any other field.

    ``from squarefactor.admin.fields import WYSIWYGField``
    ``class SomeModel(models.Model):``
        ``my_field_name = WYSIWYGField()``
    
    Make sure you have 'squarefactor.admin' in your INSTALLED_APPS or 
    the templates won't be found.
    
    1. When configuring TinyMCE  use the class name 'wysiwyg' as your hook. 
      ``tinyMCE.init({``
          ``mode : "specific_textareas",``
          ``editor_selector : "wysiwyg",``
          ...

    2. We also assume two javscript files are in your media folder:

      `/media/js/tiny_mce/tiny_mce.js`
      `/media/js/wysiwyg.js`

      if these files are missing you'll get an ordinary text field.

  """

  class Media:
    # We could probably include a default tinymce config if we wrote a template tag for the contents
    # of wysiwyg.js this way we could include the necessary js in the template file but account for
    # multiple editors in one form and not spit the js out more than once.

    js = [settings.MEDIA_URL + "js/tiny_mce/tiny_mce.js", settings.MEDIA_URL + "js/wysiwyg.js"]

  def render(self, name, value, attrs=None):
    return render_to_string("wysiwyg.html", locals())

class TemplatePickerSelect(Select):
  """
  Select widget with choices prepopulated with all available templates.
  This searches any template directory for installed apps
  template_dirs should be None or a list of directories relative to TEMPLATE_DIRS
  template_dirs=None means include all template dirs and subfolders
  
  """
  def __init__(self, attrs=None, choices=(),
               patterns=['*.py','*.html','*.htm','*.txt'],
               inc_template_dirs=None):
    super(TemplatePickerSelect, self).__init__(attrs)
    if len(choices) == 0:
      import os, fnmatch
      templates = []
      choices = []
      # get all the available template directory specified apps in INSTALLED_APPS
      from django.template.loaders.app_directories import app_template_dirs
      from sets import Set
      _template_dirs = list(settings.TEMPLATE_DIRS) + list(app_template_dirs)
      template_dirs = []
      for template_dir in _template_dirs:
        template_dirs.append(os.path.abspath(template_dir))
      template_dirs = list(set(template_dirs))
      for template_dir in template_dirs:
        for path, dirs, files in os.walk(os.path.abspath(template_dir)):
          p = path.rsplit(os.sep)[-1]
          if p[0] == '.': # skip hidden directories
            continue
          if inc_template_dirs is None or p in inc_template_dirs:
            for file in files:
              if file[0] != '.': # skip hidden files
                for pattern in patterns:
                  if fnmatch.fnmatch(file, pattern):
                    # we only want everything after the part that is template_dir
                    templates.append(os.path.join(path, file).replace(template_dir + '/', ''))
      templates.sort()
      for template in templates:
        if not template.startswith('admin'): # exclude admin templates
          choices.append((template, template))
    self.choices = [('','')] + choices


class GeoLocationFieldWidget(AdminTextareaWidget):
  """ 
  The widget used to render the GeoLocationField in the admin.
  Allows fine tuning of a geo-coded address with a clickable google map.
  
  Assumes that the required js files are in the media js folder.
    * jquery.js
    * query.json-1.3.min.js
    * geo_location_field.js
  
  Also assumes that the google maps api key is in the settings file under GOOGLE_MAPS_API_KEY.
  """
  
  def __init__(self, attrs=None):
    super(GeoLocationFieldWidget, self).__init__(attrs)
  
  def render(self, name, value, attrs=None):
    return render_to_string("geo_location_field.html", locals())
  
  class Media:
    try:
      js = ['js/jquery.js', 'js/geo_location_field.js', 'js/jquery.json-1.3.min.js',  'http://maps.google.com/maps?file=api&amp;v=2&amp;key=' + settings.GOOGLE_MAPS_API_KEY]
    except AttributeError:
      pass
