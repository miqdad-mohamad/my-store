from pathlib import Path
import os
from pathlib import Path
from dotenv import load_dotenv
import dj_database_url

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent


# SECURITY WARNING: keep the secret key used in production secret!, handeled via .env
SECRET_KEY = os.environ.get('SECRET_KEY')
# SECURITY WARNING: DEBUG must be False in production (Handled via .env on Render)
DEBUG = os.environ.get('DEBUG') == 'True'

ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '').split(',')


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'store',
    'cloudinary_storage',
    'cloudinary',
    'rest_framework',
    'rest_framework.authtoken',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'mystore.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'mystore.wsgi.application'


# Database configuration
# Use SQLite if DATABASE_URL is not set, otherwise use PostgreSQL
DATABASES = {
    'default': dj_database_url.config(
        default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}",
        conn_max_age=600,
        # Disable SSL if connecting to a local Docker database
        ssl_require=os.environ.get(
            'DATABASE_URL') and 'db' not in os.environ.get('DATABASE_URL', '')
    )
}


AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Base URL for serving static files (CSS, JS, Images) to the browser
STATIC_URL = '/static/'

# Physical directory where Django looks for static files during development
STATICFILES_DIRS = [BASE_DIR / 'static']

# Base URL for user-uploaded files (e.g., product images)
MEDIA_URL = '/media/'

# Physical directory where uploaded files are stored
MEDIA_ROOT = BASE_DIR / 'media'

# Define the root directory where static files will be collected for production
STATIC_ROOT = BASE_DIR / 'staticfiles'


# Use local storage during development to avoid external dependencies (like VPNs).
# Switch to Cloudinary in production to ensure media files persist across deployments.
if DEBUG:
    STORAGES = {
        "default": {
            # Store media files locally on the file system during development
            "BACKEND": "django.core.files.storage.FileSystemStorage",
        },
        "staticfiles": {
            # Compress and cache static files using WhiteNoise
            "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
        },
    }
else:
    STORAGES = {
        "default": {
            # Use Cloudinary's global CDN for permanent media storage in production
            "BACKEND": "cloudinary_storage.storage.MediaCloudinaryStorage",
        },
        "staticfiles": {
            # Compress and cache static files using WhiteNoise
            "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
        },
    }


REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'store.permissions.IsAdminOrStaffOrReadOnly',
    ],
}


if not DEBUG:
    # Force all traffic to use secure HTTPS connections.
    SECURE_SSL_REDIRECT = True

    # Ensure session cookies are only sent over HTTPS to prevent interception.
    SESSION_COOKIE_SECURE = True

    # Ensure CSRF cookies are only sent over HTTPS to prevent token theft.
    CSRF_COOKIE_SECURE = True

    # Enable HTTP Strict Transport Security (HSTS) for one year (31536000 seconds).
    SECURE_HSTS_SECONDS = 31536000

    # Apply the HSTS policy to all subdomains.
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True

    # Allow browsers to preload the HSTS policy.
    SECURE_HSTS_PRELOAD = True

    # Prevent browsers from MIME-sniffing (protects against certain XSS attacks).
    SECURE_CONTENT_TYPE_NOSNIFF = True

    # Enable the browser's built-in XSS filtering (Defense in depth).
    SECURE_BROWSER_XSS_FILTER = True

    # Prevent the site from being embedded in an iframe (Mitigates Clickjacking).
    X_FRAME_OPTIONS = 'DENY'

    # Crucial for platforms like Render: Tells Django that the original request was HTTPS,
    # even though the load balancer forwards it internally as HTTP.
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
