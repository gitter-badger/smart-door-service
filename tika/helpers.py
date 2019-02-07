from django.conf import settings


def trim(string):
    return string.replace('"', '')


def get_rounds():
    return getattr(settings, "BCRYPT_ROUNDS", 12)
