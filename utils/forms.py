from django import forms
from django.forms.widgets import *
from django.forms.util import ValidationError

import datetime

class TimeDropdownWidget(forms.MultiWidget):
  def __init__(self, attrs=None, hour_range=None, minute_range=None, include_blanks=False):
    HOURS = hour_range or xrange(1, 13)
    MINUTES = minute_range or xrange(0, 60)

    hours = map(lambda x:(x, x), HOURS)
    minutes = []
    for m in MINUTES:
      if m < 10:
        minutes.append((m,'0' + str(m)))
      else:
        minutes.append((m,m))
    if include_blanks:
      hours.insert(0, ('', ''))
      minutes.insert(0, ('', ''))
    widgets = (
      forms.Select(choices=hours),
      forms.Select(choices=minutes),
      forms.Select(choices=[('',''), ('am','am'), ('pm','pm')])
    )
    super(TimeDropdownWidget, self).__init__(widgets, attrs)

  def format_output(self, widgets):
    format = "%s : %s %s".decode('utf-8')
    return format%(widgets[0], widgets[1], widgets[2])

  def decompress(self, value):
    if value != None:
      ampm = 'am'
      try:
        value + ''
        hour, minutes, seconds = value.split(':')
        hour = int(hour)
        minutes = int(seconds)
      except:
        hour = value.hour
        minutes = value.minute
      if hour > 12:
        ampm = 'pm'
        hour = hour - 12
      elif hour == 0:
        hour = 12
      return [hour, minutes, ampm]
    return [None,None, None]

class TimeDropdownField(forms.MultiValueField):
  def __init__(self, *args, **kwargs):
    fields = (
      forms.IntegerField(required=False),
      forms.IntegerField(required=False),
      forms.CharField(required=False)
    )
    super(TimeDropdownField, self).__init__(fields, *args,**kwargs )
  
  def clean(self, value):
    if value:
      if value[0] and value[1] and value[2]:
        return self.compress(value)
      elif not value[0] and not value[1] and not value[2]:
        return self.compress(['','',''])
      else:
        raise ValidationError(u'Select a value for all time pieces or leave them all blank')
  
  def compress(self, data_list):
    if data_list and len(data_list) == 3:
      hour = data_list[0]
      minutes = data_list[1]
      ampm = data_list[2]
      if hour:
        hour = int(hour)
        if ampm == 'pm' and hour != 12:
          hour = hour + 12
        elif ampm == 'am' and hour == 12:
          hour = 0
      if hour and minutes:
        minutes = int(minutes)
        return datetime.time(hour, minutes, 0)
    return None
