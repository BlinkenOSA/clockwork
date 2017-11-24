# User Authentication
AUTHENTICATION_BACKENDS = (
    'userena.backends.UserenaAuthenticationBackend',
    'guardian.backends.ObjectPermissionBackend',
    'django.contrib.auth.backends.ModelBackend',
)

ANONYMOUS_USER_ID = -1
AUTH_PROFILE_MODULE = 'accounts.UserProfile'
SITE_ID = 1

LOGIN_URL = '/accounts/signin/'
LOGOUT_URL = '/accounts/signout/'

USERENA_SIGNIN_REDIRECT_URL = '/'
USERENA_REDIRECT_ON_SIGNOUT = '/accounts/signin/'
USERENA_DISABLE_PROFILE_LIST = True
USERENA_ACTIVATION_REQUIRED = False
USERENA_DISABLE_SIGNUP = True
USERENA_USE_MESSAGES = False
USERENA_MUGSHOT_PATH = 'mugshots/%(username)s/'
USERENA_DEFAULT_PRIVACY = 'open'
USERENA_REGISTER_PROFILE = False
