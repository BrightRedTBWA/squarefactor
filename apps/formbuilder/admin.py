from django.conf import settings
from django.contrib import admin

from squarefactor.apps.formbuilder.models import FormBuilder, FormBuilderField, FormBuilderFieldType, \
                                                 FormSubmission

class FormBuilderFieldInline(admin.StackedInline):
  model = FormBuilderField
  extra = 5

class FormBuilderAdmin(admin.ModelAdmin):
  inlines = [FormBuilderFieldInline]
  save_on_top = True
  
  class Media:
    js = [
      settings.MEDIA_URL + 'js/jquery.js',
      settings.MEDIA_URL + 'js/ui.core.min.js',
      settings.MEDIA_URL + 'js/ui.sortable.min.js',
      settings.MEDIA_URL + 'js/menu-sort.js',
    ]
  
admin.site.register(FormBuilder, FormBuilderAdmin)

admin.site.register(FormBuilderFieldType)

class FormSubmissionAdmin(admin.ModelAdmin):
  fieldsets = (
    (None, {'fields': ('form', 'message',)}),
  )
  list_filter = ('form',)
  date_hierarchy = 'date_submitted'

admin.site.register(FormSubmission, FormSubmissionAdmin)
