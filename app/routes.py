import os
from django.conf.urls import url, include
from app.http.controllers import \
    door_controller,\
    system_controller,\
    home_controller,\
    login_controller,\
    logs_controller

urlpatterns = [

    # View routes
    url(r'^$', home_controller.index),

    # Api routes
    url("api", include([

        # System information route
        url("system.json", system_controller.check),

        # Api version route
        url(os.getenv("APP_VERSION"), include([

            # Auth routes
            url('auth', include([
                url('create.json', login_controller.create),
                url('refresh.json', login_controller.refresh)
            ])),

            # Handle gpio (door) pin with door route
            url('door/open.json', door_controller.open_door),

            # User data routes
            url('user', include([
                url('logs.json', logs_controller.index),
            ])),

        ])),
    ]))
]
