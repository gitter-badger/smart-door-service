# -*- coding: utf-8 -*-
from app.models import *
from app.http import middlewares
from django.shortcuts import render
from django.utils.decorators import decorator_from_middleware
from django.views.decorators.csrf import csrf_exempt, csrf_protect


@decorator_from_middleware(middlewares.DashboardAuthenticate)
def index(request):
    return render(request, 'dashboard/settings.html', {
        "page": "settings"
    })
