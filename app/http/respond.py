import json
from django.core import serializers
from django.http import HttpResponse


def succeed(data):
    content = json.dumps({"status": "success", "result": data})
    return HttpResponse(content, content_type="application/json", status=200)


def succeed_message(message):
    content = json.dumps({"status": "success", "message": message})
    return HttpResponse(content, content_type="application/json", status=200)


def model_datas(datas):
    results = []
    for data in json.loads(serializers.serialize('json', datas)):
        results.append(data['fields'])
    return results


def update_succeeded():
    return succeed("The requested parameter is updated successfully!")


def insert_succeeded():
    return succeed("The requested parameter is Added successfully!")


def failed(message, status_code=400):
    content = json.dumps({"status": "fail", "message": message})
    return HttpResponse(content, content_type="application/json", status=status_code)


def method_not_allowed(message="Oops... The method you requested is not allowed!"):
    return failed(message, 405)


def validation_error(errors=None, status_code=422):
    content = json.dumps({"status": "failed", "result": errors})
    return HttpResponse(content, content_type="application/json", status=status_code)


def unauthorized(message="Unauthorized."):
    return failed(message, 401)


def not_found(message="Oops... The requested page not found!"):
    return failed(message, 404)
