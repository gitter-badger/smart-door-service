import string
import platform
from .helpers import *
from . import respond


def check(request):

    scheme = request.is_secure() and "https://" or "http://"
    uri = scheme + request.META['HTTP_HOST']
    machine = os.uname()[4]

    avatars_base_uri = uri + "/uploads/avatars"

    if os.getenv("AVATARS_URI") is not None and os.getenv("AVATARS_URI") is not "":
        avatars_base_uri = os.getenv("AVATARS_URI")

    return respond.succeed({
        "version": os.getenv("APP_VERSION"),
        "base_uri": uri,
        "api_base_uri": uri + "/" + os.getenv("APP_VERSION"),
        "avatars_base_uri": avatars_base_uri,
        "system": {
            "name": platform.system(),
            "machine": machine
        }
    })
