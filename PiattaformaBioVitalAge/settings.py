"""
Django Settings file
"""

from pathlib import Path
import os
from os import getenv
import pymysql # type: ignore



pymysql.install_as_MySQLdb()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-1-exzg2a%&(t%r6^7*u+732h)8^z96-72gr!fk@$-ev25-zx7)'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Recupera i valori delle variabili d'ambiente
elastic_beanstalk_domain = os.getenv('ELASTIC_BEANSTALK_DOMAIN')
load_balancer_dns = os.getenv('LOAD_BALANCER_DNS')

# Imposta ALLOWED_HOSTS in base alle variabili d'ambiente
ALLOWED_HOSTS = [elastic_beanstalk_domain, load_balancer_dns, 'localhost', '127.0.0.1']
ALLOWED_HOSTS = ['*']


# Application definition
INSTALLED_APPS = [
    "admin_reorder",
    'Calcolatore',
    'BioVitalAge',
    'social_django',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'drf_spectacular',
]

MIDDLEWARE = [
    "admin_reorder.middleware.ModelAdminReorder",
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
]

ROOT_URLCONF = 'PiattaformaBioVitalAge.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'PiattaformaBioVitalAge.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'db_produzione',  
        'USER': 'admin',  
        'PASSWORD': 'MysqlWork_2025',  
        'HOST': 'db-produzione.cliaiq44ssq9.us-east-1.rds.amazonaws.com', 
        'PORT': '3306',
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'"
        }
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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

#AUTH_USER_MODEL = 'BioVitalAge.UtentiRegistratiCredenziali'

# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')


# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


SESSION_EXPIRE_AT_BROWSER_CLOSE = True

AUTHENTICATION_BACKENDS = (
    'BioVitalAge.backends.UtentiCredenzialiBackend',
    'social_core.backends.google.GoogleOAuth2',
    'django.contrib.auth.backends.ModelBackend',
)

LOGIN_URL = 'loginPage'
LOGIN_REDIRECT_URL = 'HomePage'

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = "596437252615-8o49l67l9jeuciqbjeh5djcdgsb5tmdv.apps.googleusercontent.com"
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = "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"
SOCIAL_AUTH_GOOGLE_OAUTH2_SCOPE = ['https://www.googleapis.com/auth/userinfo.email', 'https://www.googleapis.com/auth/userinfo.profile', 'https://www.googleapis.com/auth/gmail.readonly']
SOCIAL_AUTH_GOOGLE_OAUTH2_EXTRA_DATA = [
    'first_name', 'last_name',
    'refresh_token', 'expires_in', 'token_type', 'id_token'
]
SOCIAL_AUTH_GOOGLE_OAUTH2_AUTH_EXTRA_ARGUMENTS = {
    'access_type': 'offline',
    'prompt': 'consent'
}
SOCIAL_AUTH_REVOKE_TOKENS_ON_DISCONNECT = True
SOCIAL_AUTH_PIPELINE = (
    'social_core.pipeline.social_auth.social_details',
    'social_core.pipeline.social_auth.social_uid',
    'social_core.pipeline.social_auth.auth_allowed',
    'social_core.pipeline.social_auth.social_user',
    'social_core.pipeline.user.get_username',
    'social_core.pipeline.user.create_user',
    # Qui puoi aggiungere una funzione personalizzata:
    'social_core.pipeline.social_auth.associate_user',
    'social_core.pipeline.social_auth.load_extra_data',
    'social_core.pipeline.user.user_details',
)
CSRF_COOKIE_SAMESITE = 'Lax'
SESSION_COOKIE_SAMESITE = 'Lax'
CSRF_COOKIE_HTTPONLY = False  # Necessario per leggere il token via JS
# SESSION_COOKIE_SECURE = True  # Se usi HTTPS
CSRF_TRUSTED_ORIGINS = ['http://127.0.0.1:8000', 'http://biovitalageplatformdeployed-env.eba-exhbgdpt.us-east-1.elasticbeanstalk.com']  # I tuoi domini
CORS_ALLOW_CREDENTIALS = True


ADMIN_REORDER = [
    # 1) Dottori registrati
    {
        "app": "BioVitalAge",
        "label": "Dottori Registrati",
        "models": [
            "BioVitalAge.UtentiRegistratiCredenziali",
        ],
    },
    # 2) Elenco Cartelle Pazienti
    {
        "app": "BioVitalAge",
        "label": "Elenco Cartelle Pazienti",
        "models": [
            "BioVitalAge.TabellaPazienti",
        ],
    },
    # 3) Dettagli Cartelle Pazienti
    {
        "app": "BioVitalAge",   # ← aggiungi questa riga
        "label": "Dettagli Cartelle Pazienti",
        "models": [
            "BioVitalAge.RefertiEtaBiologica",
            "BioVitalAge.DatiEstesiRefertiEtaBiologica",
            "BioVitalAge.RefertiEtaMetabolica",
            "BioVitalAge.RefertiCapacitaVitale",
            "BioVitalAge.DatiEstesiRefertiCapacitaVitale",
            "BioVitalAge.PrescrizioniEsami",
            "BioVitalAge.ValutazioneMS",
            "BioVitalAge.Resilienza",
        ],
    },
    # 4) Appuntamenti
    {
        "app": "BioVitalAge",
        "label": "Appuntamenti",
        "models": [
            "BioVitalAge.Appointment",
        ],
    },
    {
        "app": "BioVitalAge",
        "label": "PDF esami",
        "models": [
            "BioVitalAge.AllegatiLaboratorio",
            "BioVitalAge.AllegatiStrumentale",
        ],
    },
    # 5) Calcolatore rimane in fondo
    "Calcolatore",
    # 6) Social Auth
    "social_django",
]


REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

SPECTACULAR_SETTINGS = {
    'TITLE': 'BioVitalAge API',
    'DESCRIPTION': 'Documentazione OpenAPI per le API di Cartella Paziente',
    'VERSION': '1.0.0',
}