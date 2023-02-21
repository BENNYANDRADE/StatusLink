from .base import *
import environ
environ.Env.read_env()
import dj_database_url
from decouple import config

# =================SHOW_TOOLBAR=================
def show_toolbar(request):
	return False

# =================DEBUG=================
DEBUG = os.environ.get('DEBUG')


# =================SECRET_KEY=================
SECRET_KEY = os.environ.get('SECRET_KEY')


# =================DATABASE=================
#REMOTE SERVER
DATABASES = {
	'default' : dj_database_url.config( default=config('DATABASE_URL'),conn_max_age=600,ssl_require=True)
}
#LOCAL SERVER
# DATABASES = {
# 	'default' : dj_database_url.config( default=config('DATABASE_URL'),conn_max_age=600,ssl_require=False)
# }
# DATABASES['default']['ATOMIC_REQUESTS'] = True
# DATABASES = {
# 	'default': {
# 		'ENGINE': 'django.db.backends.sqlite3',
# 		'NAME': 'StatusLink',
# 	}
# }
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# =================SECURITY=================
ALLOWED_HOSTS = [
	# "apiinstance.onrender.com",
	# "statuslink.onrender.com",
	# "statuslink.onrender.com",
	"statuslink-ft4r.onrender.com",
	# "statuslink.onrender.com",
	"localhost",
	"0.0.0.0",
	"127.0.0.1",
	"172.20.10.2",
]


# =================TEMPLATES=================
TEMPLATES[0]['OPTIONS']['debug'] = DEBUG  # NOQA


# =================CACHES=================
CACHES = {
	'default': {
		'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
		'LOCATION': '',
	}
}
# =================EMAIL=================
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_HOST = 'localhost'
EMAIL_PORT = 1025

# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = 'send.one.com'
# EMAIL_PORT = '587'
# EMAIL_HOST_USER = 'noreply@gohives.com'
# EMAIL_HOST_PASSWORD = 'Bennya'
# EMAIL_USE_TLS = True

# =================APPS=================
INSTALLED_APPS += ['django_extensions','debug_toolbar','gunicorn']


MIDDLEWARE += [
	'debug_toolbar.middleware.DebugToolbarMiddleware',
]


DEBUG_TOOLBAR_PANELS = [
	'debug_toolbar.panels.history.HistoryPanel',
	'debug_toolbar.panels.versions.VersionsPanel',
	'debug_toolbar.panels.timer.TimerPanel',
	'debug_toolbar.panels.settings.SettingsPanel',
	'debug_toolbar.panels.headers.HeadersPanel',
	'debug_toolbar.panels.request.RequestPanel',
	'debug_toolbar.panels.sql.SQLPanel',
	'debug_toolbar.panels.staticfiles.StaticFilesPanel',
	'debug_toolbar.panels.templates.TemplatesPanel',
	'debug_toolbar.panels.cache.CachePanel',
	'debug_toolbar.panels.signals.SignalsPanel',
	'debug_toolbar.panels.logging.LoggingPanel',
	'debug_toolbar.panels.redirects.RedirectsPanel',
	'debug_toolbar.panels.profiling.ProfilingPanel',
]


DEBUG_TOOLBAR_CONFIG = {
	'INTERCEPT_REDIRECTS':False,
	'SHOW_TOOLBAR_CALLBACK': show_toolbar
}