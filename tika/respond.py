import json
from django.http import HttpResponse


def succeed(data):
    content = json.dumps({"status": "success", "result": data})
    return HttpResponse(content, content_type="application/json", status=200)


def update_succeeded():
    return succeed("The requested parameter is updated successfully!")


def failed(message="", status_code=400):
    content = json.dumps({"status": "failed", "message": message})
    return HttpResponse(content, content_type="application/json", status=status_code)


def healthy():
    return succeed("Server is healthy.")


def unauthorized():
    return failed("Unauthorized.")


def not_found(message="Oops... The requested page not found!"):
    return failed(message, 404)
