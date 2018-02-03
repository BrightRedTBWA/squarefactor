from django.contrib import admin
from squarefactor.apps.events.models import Event, EventCalendar

class EventCalendarAdmin(admin.ModelAdmin):
  prepopulated_fields = {'slug': ['title']}
  search_fields = ['title']
  list_filter = ['is_default']

class EventAdmin(admin.ModelAdmin):
  search_fields = ['title', 'description']
  list_filter = ['starts', 'ends', 'all_day_event']
  date_hierarchy = 'starts'
  filter_horizontal = ['invited_users']
  
admin.site.register(EventCalendar, EventCalendarAdmin)
admin.site.register(Event, EventAdmin)