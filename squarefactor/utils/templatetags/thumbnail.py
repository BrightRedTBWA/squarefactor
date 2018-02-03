import os, re
from PIL import Image
from django import template
from django.conf import settings

register = template.Library()

"""Thumbnail filter based on code from
http://batiste.dosimple.ch/blog/2007-05-13-1/. First hacked on
http://www.stereoplex.com/two-voices/a-django-image-thumbnail-filter
hacked further by Nido Media, hacked further by james """

THUMBNAILS = 'thumbnails'
SCALE_WIDTH = 'w'
SCALE_HEIGHT = 'h'

def scale(max_x, pair):
  """scales pair. Say pair is (x, y). The returned pair will be
  (max_x, ''y scaled by max_x / x'')"""
  x, y = pair
  new_y = max_x * y / x
  return (int(max_x), int(new_y))

@register.filter
def thumbnail(image, arg):
  """ Checks if a thumbnail image already exists. If not, one is
  created. The thumbnail will reside in the thumbnail folder
  relative to the original image path, and bears an indication of it's
  new size. This filter will return the URL of the thumbnail image.
  TODO: This filter may not be thread safe"""
  if not image:
    return ''

  original_image_path = settings.MEDIA_ROOT + image.__str__()
  if not os.path.isfile(original_image_path):
    return ''

  original_image_url = image.url
  size = arg

  if image.width < image.height:
    mode = SCALE_HEIGHT
  else:
    mode = SCALE_WIDTH

  # defining the size
  max_size = int(size.strip())

  # defining the file name and the miniature file name
  basename, format = original_image_path.rsplit('.', 1)
  basename, name = basename.rsplit(os.path.sep, 1)

  miniature = name + '_' + str(max_size) + '.' + format
  thumbnail_path = os.path.join(basename, THUMBNAILS)
  if not os.path.exists(thumbnail_path):
    os.mkdir(thumbnail_path)

  miniature_filename = os.path.join(thumbnail_path, miniature)
  baseurl, crud = original_image_url.rsplit('/', 1)
  miniature_url = '/'.join((baseurl, THUMBNAILS, miniature))

  # if the image wasn't already resized, resize it
  if (not os.path.exists(miniature_filename)
      or os.path.getmtime(original_image_path) > os.path.getmtime(miniature_filename) ):
    image = Image.open(original_image_path)
    image_x, image_y = image.size

    if mode == SCALE_HEIGHT:
      image_y, image_x = scale(max_size, (image_y, image_x))
    else:
      image_x, image_y = scale(max_size, (image_x, image_y))

    image = image.resize((image_x, image_y), Image.ANTIALIAS)

    image.save(miniature_filename, image.format)

  return miniature_url
