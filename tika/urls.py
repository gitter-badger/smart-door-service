import os
from . import door_controller
from . import jwt_controller
from . import room_controller
from . import system_controller
from django.conf.urls import url, include

urlpatterns = [
    url(os.getenv("APP_VERSION"), include([

        url('health.json', system_controller.health),

        url('door/open.json', door_controller.open_door),

        url('room/lights.json', room_controller.lights),

        url('auth', include([
            url('create.json', jwt_controller.create),
            url('refresh.json', jwt_controller.refresh)
        ])),

    ])),
]
