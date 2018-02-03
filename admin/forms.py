from django import forms
from django.forms import fields
from django.utils import simplejson

class GeoLocationFormField(fields.Field):
  """ 
  Used to validate the data submitted by the GeoLocationFieldWidget in the admin.
  """
  
  def clean(self, value):
    """ 
    Validates the json submitted and the required properties.
    """
    if super(GeoLocationFormField, self).clean(value):
      
      try:
        data = simplejson.JSONDecoder().decode(value)
      except ValueError:
        # This should never happen, but if by chance the front end builds bad json, we catch it here. The user has no options if this is happening, we willneed to find the bug.
        raise forms.ValidationError('An error has occured. Unable to parse the geo encoded data for saving.')
      
      # Now make sure the json has all of the required properties to save.
      if not data['address'] or len(data['address']) < 1:
        raise forms.ValidationError('Please provide a location or address.')
      
      if not data['latitude'] or len(data['latitude']) < 1 or not data['longitude'] or len(data['longitude']) < 1:
        raise forms.ValidationError('Please wait for the geo encoding of your location to complete before clicking save.')
    
    return value