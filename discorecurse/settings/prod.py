from .base import *

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# default logging doesn't log to console with DEBUG=False
# see https://github.com/django/django/blob/main/django/utils/log.py
# override i.e. always log to console
LOGGING["handlers"]["console"] = {
    "class": "logging.StreamHandler",
}
