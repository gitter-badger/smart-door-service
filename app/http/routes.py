import os
from django.conf.urls import url, include

from django.contrib.staticfiles.urls import\
    staticfiles_urlpatterns

# view controllers
from app.http.controllers import \
    dashboard, users, logs, settings, doc

# api controllers
from app.http.controllers.api import \
    auth as api_auth, \
    door as api_door, \
    logs as api_logs, \
    system as api_system,\
    accessories as api_accessories

from django.contrib.auth import views

# Dashboard view routes
view_routes = [
    url(r'^$', dashboard.index, name='dashboard'),
    url(r'^users$', users.index, name='users'),
    url(r'^users/add$', users.create, name='add_user_form'),
    url(r'^logs$', logs.index, name='logs'),
    url(r'^doc$', doc.index, name='doc'),
    url(r'^settings$', settings.index, name='settings'),
    url(r'^login$', views.LoginView.as_view(template_name='authentication/login.html'), name='login'),
    url(r'^logout$', views.LogoutView.as_view(), name='logout'),
]

# Api routes
api_routes = [
    url("api", include([

        # System information route
        url("system.json", api_system.check),

        # Api version route
        url(os.getenv("APP_VERSION"), include([

            # Auth routes
            url('auth', include([
                url('create.json', api_auth.create),
                url('refresh.json', api_auth.refresh)
            ])),

            # Handle gpio (door) pin with door route
            url('door/open.json', api_door.open_door),

            url('accessories.json', api_accessories.index),

            # User data routes
            url('user', include([
                url('logs.json', api_logs.index),
            ])),

        ])),
    ]))
]

urlpatterns = view_routes + api_routes

# Adding static files
urlpatterns += staticfiles_urlpatterns()
