from pathlib import Path
import os
from dotenv import load_dotenv   # solo si usas python-dotenv localmente (opcional)

# Carga el .env cuando trabajas fuera de Docker
load_dotenv()

# --------------------------------------------------
# Rutas base
# --------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent

# --------------------------------------------------
# Seguridad y depuración
# --------------------------------------------------
SECRET_KEY = os.getenv(
    "DJANGO_SECRET",
    "django-insecure-p%65@x8#*t(e*)sc6k+))5+asz!*%#pdu2e@=f=pgp1_vvy8ny",  # fallback dev
)
DEBUG = os.getenv("DJANGO_DEBUG", "True") == "True"

ALLOWED_HOSTS = [
    "localhost",
    "127.0.0.1",
    "dmrede21.jcarlos19.com",
]

CSRF_TRUSTED_ORIGINS = [
    "http://dmrede21.jcarlos19.com:8000",
]

# --------------------------------------------------
# Aplicaciones
# --------------------------------------------------
INSTALLED_APPS = [
    # Django core
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Terceros
    "social_django",            # ← login GitHub / Discord
    # Propias
    "cuentas",
    "productos",
    "carrito",
    "ordenes",
    "categorias",
    "ecommerce",
]

# --------------------------------------------------
# Middlewares
# --------------------------------------------------
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# --------------------------------------------------
# Templates
# --------------------------------------------------
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "plantillas"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                # Social Auth
                "social_django.context_processors.backends",
                "social_django.context_processors.login_redirect",
            ],
        },
    },
]

# --------------------------------------------------
# URL / WSGI
# --------------------------------------------------
ROOT_URLCONF = "proyecto.urls"
WSGI_APPLICATION = "proyecto.wsgi.application"

# --------------------------------------------------
# Base de datos (PostgreSQL vía docker-compose)
# --------------------------------------------------
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("DB_NAME", "ulloadb"),
        "USER": os.getenv("DB_USER", "ullouser"),
        "PASSWORD": os.getenv("DB_PASSWORD", "ullopass"),
        "HOST": os.getenv("DB_HOST", "db"),
        "PORT": 5432,
    }
}

# --------------------------------------------------
# Usuarios
# --------------------------------------------------
AUTH_USER_MODEL = "cuentas.Cuenta"

AUTHENTICATION_BACKENDS = (
    "social_core.backends.github.GithubOAuth2",
    "social_core.backends.discord.DiscordOAuth2",
    "django.contrib.auth.backends.ModelBackend",
)

# --------------------------------------------------
# Social Auth – credenciales desde .env
# --------------------------------------------------
SOCIAL_AUTH_GITHUB_KEY    = os.getenv("GITHUB_KEY")
SOCIAL_AUTH_GITHUB_SECRET = os.getenv("GITHUB_SECRET")

SOCIAL_AUTH_DISCORD_KEY    = os.getenv("DISCORD_KEY")
SOCIAL_AUTH_DISCORD_SECRET = os.getenv("DISCORD_SECRET")

# Datos básicos que pedimos
SOCIAL_AUTH_GITHUB_SCOPE = ["read:user", "user:email"]

SOCIAL_AUTH_PIPELINE = (
    "social_core.pipeline.social_auth.social_details",
    "social_core.pipeline.social_auth.social_uid",
    "social_core.pipeline.social_auth.auth_allowed",
    "social_core.pipeline.social_auth.social_user",
    "social_core.pipeline.user.get_username",

    "cuentas.pipelines.populate_required_fields",  # ← nuestro paso

    "social_core.pipeline.user.create_user",
    "cuentas.pipelines.activate_user",             # activa la cuenta
    "social_core.pipeline.social_auth.associate_user",
    "social_core.pipeline.social_auth.load_extra_data",
)

SOCIAL_AUTH_DISCORD_SCOPE = ["identify", "email"]

SOCIAL_AUTH_GITHUB_REDIRECT_URI = "http://localhost:8000/oauth/complete/github/"

# Redirecciones
LOGIN_URL = "iniciar_sesion"
LOGIN_REDIRECT_URL = "inicio"
LOGOUT_REDIRECT_URL = "inicio"

# --------------------------------------------------
# Archivos estáticos y media
# --------------------------------------------------
STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]

MEDIA_URL = "/imagenes/"
MEDIA_ROOT = BASE_DIR / "imagenes"

# --------------------------------------------------
# Internacionalización
# --------------------------------------------------
LANGUAGE_CODE = "es-mx"
TIME_ZONE = "America/Mexico_City"
USE_I18N = True
USE_TZ = True

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# --------------------------------------------------
# Validadores de contraseña (puedes dejarlos igual)
# --------------------------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]