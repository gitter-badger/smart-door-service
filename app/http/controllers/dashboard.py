# -*- coding: utf-8 -*-
from app.http import middlewares
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.utils.decorators import decorator_from_middleware
from django.views.decorators.csrf import csrf_exempt, csrf_protect


@csrf_exempt
@decorator_from_middleware(middlewares.DashboardAuthenticate)
def index(request):
    return render(request, 'dashboard/index.html', {
        "page": "dashboard"
    })


@csrf_exempt
@decorator_from_middleware(middlewares.DashboardAuthenticate)
def users(request):
    return render(request, 'dashboard/users.html', {
        "page": "users",
        "users": User.objects.all()
    })


@csrf_exempt
@decorator_from_middleware(middlewares.DashboardAuthenticate)
def logs(request):
    return render(request, 'dashboard/logs.html', {
        "page": "logs",
        "logs": ""
    })


@csrf_exempt
@decorator_from_middleware(middlewares.DashboardAuthenticate)
def settings(request):
    return render(request, 'dashboard/settings.html', {
        "page": "settings"
    })
