from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.db import models

class ReminderMethod(models.Model):
  """
  A method that can be used to send a reminder.
  """
  
  title = models.CharField(max_length=100)
  
  class Meta:
    db_table = 'squarefactor_reminder_method'
  
  def __unicode__(self):
    return self.title

class Reminder(models.Model):
  """
  A generic reminder description that can be attached to any model.
  """
  
  method = models.ForeignKey(ReminderMethod)
  send_at = models.DateTimeField()
  
  # Generic relation fields.
  content_type = models.ForeignKey(ContentType)
  object_id = models.PositiveIntegerField()
  content_object = generic.GenericForeignKey()
  
  class Meta:
    db_table = 'squarefactor_reminder'
  
  def __unicode__(self):
    return '%s reminder' % (self.method,)

