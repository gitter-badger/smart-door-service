import json
from django.core import serializers
from django.http import HttpResponse
from django.forms.models import model_to_dict
from django.db import models
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models.fields.related import ForeignKey

def succeed(data):
    response = {"status": "success", "result": data}
    content = json.dumps(response, sort_keys=False,cls=DjangoJSONEncoder)
    return HttpResponse(content, content_type="application/json", status=200)


def succeed_message(message):
    response = {"status": "success", "message": message}
    content = json.dumps(response, sort_keys=False,cls=DjangoJSONEncoder)
    return HttpResponse(content, content_type="application/json", status=200)


def update_succeeded():
    return succeed("The requested parameter is updated successfully!")


def insert_succeeded():
    return succeed("The requested parameter is Added successfully!")


def failed(message, status_code=400):
    response = {"status": "fail", "message": message}
    content = json.dumps(response, sort_keys=False,cls=DjangoJSONEncoder)
    return HttpResponse(content, content_type="application/json", status=status_code)


def method_not_allowed(message="Oops... The method you requested is not allowed!"):
    return failed(message, 405)


def validation_error(errors=None, status_code=422):
    response = {"status": "failed", "result": errors}
    content = json.dumps(response, sort_keys=False,cls=DjangoJSONEncoder)
    return HttpResponse(content, content_type="application/json", status=status_code)


def unauthorized(message="Unauthorized."):
    return failed(message, 401)


def not_found(message="Oops... The requested page not found!"):
    return failed(message, 404)
