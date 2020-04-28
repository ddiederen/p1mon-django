"""
Django settings for p1mon project.

Generated by 'django-admin startproject' using Django 2.1.5.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'smkfgp15im=0+!l2=cmklq4lcr#u_)i_0h(qb@o7-ywf%8!e#-'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
ALLOWED_HOSTS = ['*']

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'constance',
    'constance.backends.database',
    'jchart',
    'serialdata.apps.SerialdataConfig',
    'history.apps.HistoryConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'p1mon.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'p1mon/templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.request',
            ],
        },
    },
]

WSGI_APPLICATION = 'p1mon.wsgi.application'

# Navigation
NAVIGATION_SITEMAPS = (
    'navigation.base.FlatPageSitemapInfo',
)

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'p1mon/default.db'),
    },
    'serialdata_db': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'serialdata/serialdata.db'),
    },
    'history_db': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'history/history.db'),
    },
    # 'django_q_db': {
    #     'ENGINE': 'django.db.backends.sqlite3',
    #     'NAME': os.path.join(BASE_DIR, 'django_q/django_q.db'),
    # },
}    
DATABASE_ROUTERS = [
    'p1mon.dbRouter.P1monDBRouter',
    'history.dbRouter.HistoryDBRouter',
    'serialdata.dbRouter.SerialdataDBRouter',
]

# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators
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


## Queue cluster
#Q_CLUSTER = {
#    'name': 'DjangoORM',
#    'timeout': 1200,	# Timeout in secs for a task
#    'save_limit': 10,	# Store latest 10 results only
#    'catch_up': False,	# Ignore un-run scheduled tasks
#    'orm': 'default',	# Django database connection
#    'sync': True       # All tasks sync for windows, turn off on linux!!
#}
#CACHES = {
#    'default': {
#            'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
#            'LOCATION': 'djangoq-localmem',
#    }
#}

# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/
LANGUAGE_CODE = 'en-gb'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/
STATICFILES_DIRS = [                                        # non-standard locations
    os.path.join(BASE_DIR, "p1mon/static"),
]
STATIC_ROOT = os.path.join(BASE_DIR, "static_collected")    # URL to where static files are collected
STATIC_URL = "/static/"

# Redirect to home URL after login (Default redirects to /accounts/profile/)
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

# Emails forgot password
EMAIL_BACKEND = "django.core.mail.backends.filebased.EmailBackend"
EMAIL_FILE_PATH = os.path.join(BASE_DIR, "sent_emails")

# REST API
REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    ]
}

# Constance dynamic website setting
CONSTANCE_BACKEND = 'constance.backends.database.DatabaseBackend'

CONSTANCE_IGNORE_ADMIN_VERSION_CHECK = True # Use this option in order to skip hash verification

CONSTANCE_DBS = ['default']

CONSTANCE_CONFIG = {
    'O_1': (0.218, '€/kWh verbruik uren'),
    'O_2': (0.218, '€/kWh geleverd uren'),
        
    'E_VERBRUIK_ELEK': (0.218, 'Kosten verbruik elektriciteit (€/kWh)'),
    'E_GELEVERD_ELEK': (-0.218, 'Kosten levering elektriciteit (€/kWh). Vul hier een negatief getal in, aangezien het negatieve kosten zijn.'),
    'E_VASTRECHT_ELEK': (6.1, '€ vastrecht per maand (aansluiting)'),
    
    'G_VERBRUIK_GAS': (0.748, 'Kosten verbruik gas (m3)'),
    'G_VASTRECHT_GAS': (0, '€ vastrecht per maand (aansluiting)'),
    
    'P1_BAUDRATE': (115200, 'baud rate'), 
    'P1_BYTESIZE': (8, 'databits'),
    'P1_PARITY': ("geen", 'parity'), 
    'P1_STOPBITS': (1, 'stop bits'), 

    'G_LIVE_ELEK_VERBRUIK_MAX': (10, 'Maximum verbruik elektriciteit - live [kW]'),  
    'G_LIVE_ELEK_GELEVERD_MAX': (10, 'Maximum geleverd elektriciteit - live [kW]'), 
    'G_LIVE_GAS_MAX': (10, 'Maximum gas - live [m3/u]'), 
    'G_TODAY_ELEK_VERBRUIK_MAX': (50, 'Maximum verbruik elektriciteit - live [kWh]'),   
    'G_TODAY_ELEK_GELEVERD_MAX': (50, 'Maximum geleverd elektriciteit - live [kWh]'), 
    'G_TODAY_GAS_MAX': (50, 'Maximum gas - live [m3]'), 
}

CONSTANCE_CONFIG_FIELDSETS = {
    'Opslag data': (
        'O_1', 
        'O_2',
    ),
    'Tarieven elektriciteit - zoek op bij uw energie leverancier': (
        'E_VERBRUIK_ELEK', 
        'E_GELEVERD_ELEK', 
        'E_VASTRECHT_ELEK', 
    ),
    'Tarieven gas - zoek op bij uw energie leverancier': (
        'G_VERBRUIK_GAS',
        'G_VASTRECHT_GAS', 
    ),
    'P1 poort - Data aflezen - In Nederland is het DSMR 3 protocol 9600 7E1 (7 databits, even parity, 1 stop bit) of DSMR 4 protocol 115200 8N1 (8 databits, geen parity, 1 stop bit) gebruikelijk.': (
        'P1_BAUDRATE', 
        'P1_BYTESIZE',
        'P1_PARITY', 
        'P1_STOPBITS', 
    ),
    'Grafieken - variabelen': (
        'G_LIVE_ELEK_VERBRUIK_MAX', 
        'G_LIVE_ELEK_GELEVERD_MAX',
        'G_LIVE_GAS_MAX',
        'G_TODAY_ELEK_VERBRUIK_MAX', 
        'G_TODAY_ELEK_GELEVERD_MAX',
        'G_TODAY_GAS_MAX',
    ),
}