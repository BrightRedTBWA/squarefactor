def return_json_response(o, simple=False):
  """
  Serialize to JSON.
  simplejson can't do all objects.
  serialize can't do form errors
  """
  # the serialization methods require an iterable to be passed
  try:
    # if obj isn't a list
    o + []
  except:
    # make it one
    o = [o]
  if simple:
    from django.utils import simplejson
    json = simplejson.dumps(o)
  else:
    from django.core import serializers
    json_serializer = serializers.get_serializer("json")()
    json = json_serializer.serialize(o, ensure_ascii=False)
  return HttpResponse(json, mimetype='application/javascript')

def get_error_dict(form):
  # build a dict because the proxy objects can't be directly serialized
  errors = {}
  for field in form:
    if field.errors:
      errors[field.name] = {'errors': [unicode(e) for e in field.errors]}
  return errors # return a list for consistency, objects are returned as lists