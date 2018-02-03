from django import forms
from django.conf import settings
from django.db import models
from squarefactor.admin import widgets, forms
from django.utils import simplejson

class WYSIWYGField(models.TextField):
  """ A field that renders as a WYSIWYG """
  
  def formfield(self, **kwargs):
    kwargs['widget'] = widgets.WYSIWYGTextAreaWidget
    return super(WYSIWYGField, self).formfield(**kwargs)

class MarkdownField(models.TextField):
  """ A textfield that expects markdown input. """

  def formfield(self, **kwargs):
    kwargs['widget'] = widgets.MarkdownWidget()
    return super(MarkdownField, self).formfield(**kwargs)

class TemplatePickerField(models.CharField):
  """ A field that shows a list of available templates in a select menu. """

  def __init__(self, *args, **kwargs):
    self.template_dirs = None
    if 'max_length' not in kwargs:
      kwargs['max_length'] = 255
    if 'template_dirs' in kwargs:
      self.template_dirs = kwargs['template_dirs']
      del kwargs['template_dirs']
    super(TemplatePickerField, self).__init__(*args, **kwargs)

  def formfield(self, **kwargs):
    kwargs['widget'] = widgets.TemplatePickerSelect(inc_template_dirs=self.template_dirs)
    return super(TemplatePickerField, self).formfield(**kwargs)

class ImagePreviewField(models.ImageField):
  """ A field for uploading images that will show a preview of the image """
  def formfield(self, **kwargs):
    kwargs['widget'] = widgets.ImageFileInput()
    return super(ImagePreviewField, self).formfield(**kwargs)

class GeoLocationField(models.TextField):
  """ 
  Stores an address and the google geocoded data for latitude and longitude.
  This data is automatically retrieved from google when the location is saved.
  """

  __metaclass__ = models.SubfieldBase

  def to_python(self, value):
    if not value or isinstance(value, dict):
      return value

    try:
      value = simplejson.JSONDecoder().decode(value)
    except ValueError:
      # Bad data made it into the database, we are probably screwed anyway.
      value = {}
    return value

  def get_db_prep_value(self, value):
    return simplejson.JSONEncoder().encode(value)

  def formfield(self, **kwargs):
    kwargs['widget'] = widgets.GeoLocationFieldWidget
    kwargs['form_class'] = forms.GeoLocationFormField
    return super(GeoLocationField, self).formfield(**kwargs)
