from django.contrib.auth.models import User
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.db import models
from squarefactor.admin.fields import GeoLocationField
from squarefactor.models import Reminder


class Calendar(models.Model):
  """
  A container that can be used to hold events and tied to a user.
  """
  
  private = models.BooleanField(default=False)
  slug = models.SlugField(unique=True)
  title = models.CharField(max_length=50)
  user = models.ForeignKey(User, related_name='calendars')
  is_default = models.BooleanField(default=False)
  
  class Meta:
    db_table = 'squarefactor_events_calendar'
  
  def __unicode__(self):
    return self.title
  
  def save(self):
    super(EventCalendar, self).save()
    
    # Make suere there is only one default calendar for the user.
    if self.is_default:
      EventCalendar.objects.filter(user=self.user).exclude(id=self.id).update(is_default=0)

class Event(models.Model):
  """
  An event that may be on a calendar.
  """
  
  private = models.BooleanField(default=False)
  title = models.CharField(max_length=255)
  description = models.TextField()
  starts = models.DateTimeField(blank=True, null=True)
  
  # If there is not ends value set, then it is an all day event.
  ends = models.DateTimeField(blank=True, null=True)
  
  location = GeoLocationField()
  invited_users = models.ManyToManyField(User)
  reminders = generic.GenericRelation(Reminder)
  calendar = models.ForeignKey(Calendar)
  
  class Meta:
    db_table = 'squarefactor_events_event'
  
  def __unicode__(self):
    return self.title

