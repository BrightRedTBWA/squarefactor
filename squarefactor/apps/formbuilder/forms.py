from django import forms
from django.conf import settings
from django.contrib.localflavor.us.forms import USPhoneNumberField
from django.contrib.sites.models import Site
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string

from copy import deepcopy

from squarefactor.apps.formbuilder.models import FormBuilder, FormBuilderField, FormSubmission

class FormBuilderForm(forms.ModelForm):
  class Meta:
    model = FormBuilder
    exclude = ('slug',)

class BuiltForm(forms.Form):
  submitted = False
  
  def __init__(self, *args, **kwargs):
    if 'url' in kwargs:
      url = kwargs['url']
      del kwargs['url']
      self.instance = get_object_or_404(FormBuilder, url=url)
    super(BuiltForm, self).__init__(*args, **kwargs)
    for field in self.instance.formfields.all():
      field_type = field.type.title
      field_name = field.title.replace(' ', '_').lower()
      if field_type == 'Text':
        self.base_fields[field_name] = forms.CharField()
      elif field_type == 'Email':
        self.base_fields[field_name] = forms.EmailField()
      elif field_type == 'Phone':
        self.base_fields[field_name] = USPhoneNumberField()
      elif field_type == 'BigText':
        self.base_fields[field_name] = forms.CharField(widget=forms.Textarea)
      elif field_type == 'Checkbox':
        self.base_fields[field_name] = forms.BooleanField()
      self.base_fields[field_name].label = field.title
      self.base_fields[field_name].required = field.required
      if field.help_text:
        self.base_fields[field_name].help_text = field.help_text
      if field.required_error_message:
        self.base_fields[field_name].error_messages['required'] = field.required_error_message
      if field.invalid_error_message:
        self.base_fields[field_name].error_messages['invalid'] = field.invalid_error_message
      if field.initial_data:
        self.base_fields[field_name].initial = field.initial_data
    self.fields = deepcopy(self.base_fields)
  
  def save(self):
    current_site = Site.objects.get_current()
    template = self.instance.template or 'formbuilder_email_default.txt'
    subject = self.instance.send_to_subject or 'Form Submission from %s' % current_site.name
    if 'email' in self.cleaned_data:
      from_email = self.cleaned_data['email']
    else:
      from_email = settings.DEFAULT_FROM_EMAIL
    message = render_to_string(template, {'data': self.cleaned_data})
    send_mail(subject, message, from_email, [self.instance.send_to_email])
    from django.utils import simplejson
    submission = FormSubmission.objects.create(form=self.instance,
                                               message=message,
                                               data=simplejson.dumps(self.cleaned_data))
    self.submitted = True
