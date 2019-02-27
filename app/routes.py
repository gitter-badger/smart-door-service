import os
from django.conf.urls import url, include

# view controllers
from app.http.controllers import \
    dashboard

# api controllers
from app.http.controllers.api import \
    auth, door, logs, system

from django.contrib.auth import views

# Dashboard view routes
view_routes = [
    url(r'^$', dashboard.index, name='dashboard'),
    url(r'^users', dashboard.users, name='users'),
    url(r'^logs', dashboard.logs, name='logs'),
    url(r'^settings', dashboard.settings, name='settings'),
    url(r'^login', views.LoginView.as_view(), name='login'),
    url(r'^logout', views.LogoutView.as_view(), name='logout'),
]

# Api routes
api_routes = [
    url("api", include([

        # System information route
        url("system.json", system.check),

        # Api version route
        url(os.getenv("APP_VERSION"), include([

            # Auth routes
            url('auth', include([
                url('create.json', auth.create),
                url('refresh.json', auth.refresh)
            ])),

            # Handle gpio (door) pin with door route
            url('door/open.json', door.open_door),

            # User data routes
            url('user', include([
                url('logs.json', logs.index),
            ])),

        ])),
    ]))
]

urlpatterns = view_routes + api_routes
