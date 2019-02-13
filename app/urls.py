import os
from django.urls import path
from . import door_controller
from . import login_controller
from django.conf.urls import url, include

urlpatterns = [
    url(os.getenv("APP_VERSION"), include([
        url('door/open.json', door_controller.open_door),
        url('auth', include([
            url('create.json', login_controller.create),
            url('refresh.json', login_controller.refresh)
        ])),
    ])),
]
