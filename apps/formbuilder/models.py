from django.conf import settings
from django.db import models
from django.forms.models import inlineformset_factory
from django.template.loader import render_to_string

from squarefactor.admin.fields import TemplatePickerField

class FormBuilderFieldType(models.Model):
  title = models.CharField(max_length=50)
  
  class Meta:
    ordering = ['title']
    verbose_name = 'Form field type'
  
  def __unicode__(self):
    return self.title

class FormBuilder(models.Model):
  title = models.CharField(max_length=100)
  content = models.TextField(blank=True, null=True)
  confirmation_message = models.TextField(blank=True, null=True)
  url = models.CharField(max_length=255)
  send_to_subject = models.CharField(max_length=100, blank=True)
  send_to_email = models.EmailField()
  template = TemplatePickerField(blank=True)
  
  class Meta:
    verbose_name = 'Form'
  
  def __unicode__(self):
    return self.title

class FormBuilderField(models.Model):
  form = models.ForeignKey(FormBuilder, related_name='formfields')
  title = models.CharField(max_length=100)
  type = models.ForeignKey(FormBuilderFieldType)
  required = models.BooleanField()
  required_error_message = models.CharField(max_length=100, blank=True)
  invalid_error_message = models.CharField(max_length=100, blank=True)
  initial_data = models.TextField(blank=True, null=True)
  help_text = models.CharField(max_length=100, blank=True)
  order = models.IntegerField(blank=True, null=True)
  
  class Meta:
    ordering = ['order']
  
  def __unicode__(self):
    return '%s - %s' % (self.form.title, self.title,)

class FormSubmission(models.Model):
  form = models.ForeignKey(FormBuilder)
  message = models.TextField()
  data = models.TextField()
  date_submitted = models.DateTimeField(auto_now_add=True)
  
  def __unicode__(self):
    return '%s - %s' % (self.form.title, self.date_submitted.strftime('%m/%d/%Y %H:%M %p'))
