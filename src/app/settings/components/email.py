import os

# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = 'smtp.gmail.com'
# EMAIL_USE_TLS = True
# EMAIL_PORT = 587
# EMAIL_HOST_RECIPIENT = os.environ['EMAIL_HOST_RECIPIENT']
# EMAIL_HOST_USER = os.environ['EMAIL_HOST_USER']
# EMAIL_HOST_PASSWORD = os.environ['EMAIL_HOST_PASSWORD']

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.meta.ua'
EMAIL_PORT = 465
EMAIL_STARTTLS = False
EMAIL_USE_SSL = True
EMAIL_USE_TLS = False
EMAIL_HOST_USER = os.environ['EMAIL_HOST_USER']
EMAIL_HOST_PASSWORD = os.environ['EMAIL_HOST_PASSWORD']
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
