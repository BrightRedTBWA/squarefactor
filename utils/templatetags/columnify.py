import math

from django import template
from django.conf import settings
from django.template import Node, Variable, TemplateSyntaxError, RequestContext
from django.template.loader import render_to_string

register = template.Library()

class Columnify(Node):
  def __init__(self, object_list, template, num_cols, list_var_name):
    self.object_list = Variable(object_list)
    self.template = Variable(template)
    self.num_cols = Variable(num_cols)
    self.list_var_name = Variable(list_var_name)
    
  def render(self, context):
    object_list = self.object_list.resolve(context)
    template = self.template.resolve(context)
    num_cols = self.num_cols.resolve(context)
    list_var_name = self.list_var_name.var
    wrap_after = int(math.ceil(len(object_list) / float(num_cols)))
    return render_to_string(template,
                            {'wrap_after': wrap_after, list_var_name: object_list},
                            context_instance=context)

@register.tag
def columnify(parser, token):
  """
  Usage:
  {% columnify object_list template num_cols object_list_varname %}
  or with default list variable name being a string version of what was passed in for object_list
  {% columnify object_list template num_cols %}
  or for 2 column default with list variable name being a string version of what was passed in for object_list
  {% columnify object_list template %}
  
  Your template should use a variable named wrap_after to determine where to start a new column
  The best way to do this is usually {% if forloop.counter|divisibleby:wrap_after %}new column{% endif %}
  """
  bits = token.contents.split()
  if len(bits) == 5:
    return Columnify(bits[1], bits[2], bits[3], bits[4])
  elif len(bits) == 4:
    return Columnify(bits[1], bits[2], bits[3], bits[1])
  elif len(bits) == 3:
    return Columnify(bits[1], bits[2], '2', bits[1])
  else:
    raise TemplateSyntaxError('%s tag requires at least two arguments' % bits[0])
