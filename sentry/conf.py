from django.conf import settings
from django.utils.hashcompat import md5_constructor
from django.utils.translation import ugettext_lazy as _

import logging
import socket

# Allow local testing of Sentry even if DEBUG is enabled
DEBUG = getattr(settings, 'DEBUG', False) and not getattr(settings, 'SENTRY_TESTING', False)

DATABASE_USING = getattr(settings, 'SENTRY_DATABASE_USING', None)

THRASHING_TIMEOUT = getattr(settings, 'SENTRY_THRASHING_TIMEOUT', 60)
THRASHING_LIMIT = getattr(settings, 'SENTRY_THRASHING_LIMIT', 10)

FILTERS = getattr(settings, 'SENTRY_FILTERS', (
    'sentry.filters.StatusFilter',
    'sentry.filters.LoggerFilter',
    'sentry.filters.LevelFilter',
    'sentry.filters.ServerNameFilter',
    'sentry.filters.SiteFilter',
))

KEY = getattr(settings, 'SENTRY_KEY', md5_constructor(settings.SECRET_KEY).hexdigest())

LOG_LEVELS = (
    (logging.DEBUG, _('debug')),
    (logging.INFO, _('info')),
    (logging.WARNING, _('warning')),
    (logging.ERROR, _('error')),
    (logging.FATAL, _('fatal')),
)

# This should be the full URL to sentries store view
REMOTE_URL = getattr(settings, 'SENTRY_REMOTE_URL', None)

if REMOTE_URL:
    if isinstance(REMOTE_URL, basestring):
        REMOTE_URL = [REMOTE_URL]
    elif not isinstance(REMOTE_URL, (list, tuple)):
        raise ValueError("SENTRY_REMOTE_URL must be of type list.")

REMOTE_TIMEOUT = getattr(settings, 'SENTRY_REMOTE_TIMEOUT', 5)

ADMINS = getattr(settings, 'SENTRY_ADMINS', [])

# TODO: deprecate this
USE_LOGGING = getattr(settings, 'SENTRY_USE_LOGGING', False)

if USE_LOGGING:
    default_client = 'sentry.client.log.LoggingSentryClient'
else:
    default_client = 'sentry.client.base.SentryClient'

CLIENT = getattr(settings, 'SENTRY_CLIENT', default_client)

NAME = getattr(settings, 'SENTRY_NAME', socket.gethostname())

# We allow setting the site name either by explicitly setting it with the
# SENTRY_SITE setting, or using the django.contrib.sites framework for
# fetching the current site. Since we can't reliably query the database
# from this module, the specific logic is within the SiteFilter
SITE = getattr(settings, 'SENTRY_SITE', None)

# Extending this allow you to ignore module prefixes when we attempt to
# discover which function an error comes from (typically a view)
EXCLUDE_PATHS = getattr(settings, 'SENTRY_EXCLUDE_PATHS', [])

# By default Sentry only looks at modules in INSTALLED_APPS for drilling down
# where an exception is located
INCLUDE_PATHS = getattr(settings, 'SENTRY_INCLUDE_PATHS', [])

# Absolute URL to the sentry root directory. Should not include a trailing slash.
URL_PREFIX = getattr(settings, 'SENTRY_URL_PREFIX', None)