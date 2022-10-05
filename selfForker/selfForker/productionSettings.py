from .settings import *

DEBUG = False
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True

# For whitenoise

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
STATIC_ROOT = BASE_DIR / "staticfiles"

# The solution is running locally
ALLOWED_HOSTS = ['127.0.0.1', 'localhost']
