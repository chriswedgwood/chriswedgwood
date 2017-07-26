from __future__ import absolute_import, unicode_literals

from .base import *

DEBUG = False

try:
    from .local import *
except ImportError:
    pass


GA_TRACKING_ID = 'UA-103263668-1'
