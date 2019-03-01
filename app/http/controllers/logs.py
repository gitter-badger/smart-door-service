# -*- coding: utf-8 -*-
from app import helpers
from app.models import *
from app.http import middlewares
from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage
from django.utils.decorators import decorator_from_middleware


@decorator_from_middleware(middlewares.DashboardAuthenticate)
@decorator_from_middleware(middlewares.AdminAuthenticate)
def index(request):

    page = 1
    if request.GET.get("page") is not None:
        page = request.GET.get("page")

    logs = Log.objects.all()\
        .order_by('-created_at')

    paginator = Paginator(logs, 15)

    is_empty = False
    datas = []

    try:
        datas = paginator.page(page)
    except EmptyPage:
        is_empty = True

    return render(request, 'dashboard/logs/index.html', {
        "page": "logs",
        "datas": datas,
        "is_empty": is_empty
    })
