import json
from . import respond


def health(request):
    return respond.healthy()
