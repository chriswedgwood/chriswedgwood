from __future__ import absolute_import, unicode_literals

from .base import *

DEBUG = False

try:
    from .local import *
except ImportError:
    pass


SECRET_KEY = env('DJANGO_SECRET_KEY')

GA_TRACKING_ID = 'UA-103263668-1'


DATABASES['default'] = env.db('DATABASE_URL')

ALLOWED_HOSTS = env.list('DJANGO_ALLOWED_HOSTS', default=['example.com', ])


# STORAGES
DO_SPACES_ACCESS_KEY_ID = env('DJANGO_DO_ACCESS_KEY_ID')
DO_SPACES_SECRET_ACCESS_KEY = env('DJANGO_DO_SECRET_ACCESS_KEY')
DO_SPACES_SPACE_NAME = env('DJANGO_DO_STORAGE_BUCKET_NAME') 
DO_SPACES_SPACE_FOLDER = 'mysite' # recommended: Your project name, e.g: 'blog' 
DO_SPACES_ENDPOINT_URL = 'https://fra1.digitaloceanspaces.com' # must be your Space endpoint url, e.g: 'https://sfo2.digitaloceanspaces.com' 
DO_SPACES_CACHE_MAX_AGE = 86400 
DO_SPACES_DEFAULT_ACL = None#'public-read'

# Set File locations  
DO_SPACES_STATIC_LOCATION = 'chriswedgwood/static' 
DO_SPACES_MEDIA_LOCATION = 'chriswedgwood/media'
DO_SPACES_PUBLIC_MEDIA_LOCATION = '{FOLDER}/media/public'.format(FOLDER=DO_SPACES_SPACE_FOLDER) 
DO_SPACES_PRIVATE_MEDIA_LOCATION = '{FOLDER}/media/private'.format(FOLDER=DO_SPACES_SPACE_FOLDER)

# Static files config 
STATIC_URL = 'https://{ENDPOINT_URL}/{STATIC_LOCATION}/'.format(ENDPOINT_URL=DO_SPACES_ENDPOINT_URL, STATIC_LOCATION=DO_SPACES_STATIC_LOCATION)

# Configure file storage settings 
STATICFILES_STORAGE = 'storages.backends.do_spaces.DigitalOceanSpacesStaticStorage' 
DEFAULT_FILE_STORAGE = 'storages.backends.do_spaces.DigitalOceanSpacesPublicMediaStorage' 
PRIVATE_FILE_STORAGE = 'storages.backends.do_spaces.DigitalOceanSpacesPrivateMediaStorage'

# MEDIA
# ------------------------------------------------------------------------------
#
# region http://stackoverflow.com/questions/10390244/
#from storages.backends.s3boto3 import S3Boto3Storage  # noqa E402
#StaticRootS3BotoStorage = lambda: S3Boto3Storage(location='static')  # noqa
#MediaRootS3BotoStorage = lambda: S3Boto3Storage(location='media', file_overwrite=False)  # noqa
# endregion

#MEDIA_URL = 
MEDIA_URL = 'https://{ENDPOINT_URL}/{MEDIA_LOCATION}/'.format(ENDPOINT_URL=DO_SPACES_ENDPOINT_URL, MEDIA_LOCATION=DO_SPACES_STATIC_LOCATION)
