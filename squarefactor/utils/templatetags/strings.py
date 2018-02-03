from django import template

register = template.Library()

@register.filter
def replace(value, arg):
  f, r = arg.split(',')
  f = f[1:-1]
  r = r[1:-1]
  return value.replace(f, r)
