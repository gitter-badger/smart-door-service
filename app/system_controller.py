import string
import platform
from .helpers import *
from . import respond


def check(request):

    scheme = request.is_secure() and "https://" or "http://"
    uri = scheme + request.META['HTTP_HOST']
    machine = os.uname()[4]

    return respond.succeed({
        "version": os.getenv("APP_VERSION"),
        "base_uri": uri,
        "api_base_uri": uri + "/" + os.getenv("APP_VERSION"),
        "avatars_base_uri": uri + "/uploads/avatars",
        "system": {
            "name": platform.system(),
            "machine": machine
        }
    })
