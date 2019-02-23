import string
import platform
from .helpers import *
from . import respond


def check(request):

    uri = request.scheme + "://" + request.META['HTTP_HOST']
    machine = os.uname()[4]

    if os.getenv("BASE_URI") is not None and os.getenv("BASE_URI") is not "":
        uri = os.getenv("BASE_URI")

    api_base_uri = uri + "/" + os.getenv("APP_VERSION")

    avatars_base_uri = uri + "/uploads/avatars"

    if os.getenv("API_BASE_URI") is not None and os.getenv("API_BASE_URI") is not "":
        api_base_uri = os.getenv("API_BASE_URI")

    if os.getenv("AVATARS_URI") is not None and os.getenv("AVATARS_URI") is not "":
        avatars_base_uri = os.getenv("AVATARS_URI")

    return respond.succeed({
        "version": str(os.getenv("APP_VERSION")),
        "base_uri": str(uri),
        "api_base_uri": str(api_base_uri),
        "avatars_base_uri": str(avatars_base_uri),
        "system": {
            "name": str(platform.system()),
            "machine": str(machine)
        }
    })
