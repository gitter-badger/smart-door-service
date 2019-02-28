# -*- coding: utf-8 -*-
from app.models import *
from app.http import middlewares
from django.shortcuts import render
from django.utils.decorators import decorator_from_middleware


@decorator_from_middleware(middlewares.DashboardAuthenticate)
def index(request):
    return render(request, 'dashboard/logs.html', {
        "page": "logs",
        "logs": Log.objects.all()
    })
