# -*- coding: utf-8 -*-
from app.models import *
from app.http import forms
from app.http import middlewares
from django.contrib import messages
from django.shortcuts import render, redirect
from django.utils.decorators import decorator_from_middleware
from django.views.decorators.csrf import csrf_exempt, csrf_protect


@decorator_from_middleware(middlewares.DashboardAuthenticate)
@decorator_from_middleware(middlewares.AdminAuthenticate)
def index(request):
    return render(request, 'dashboard/users/index.html', {
        "page": "users",
        "users": User.objects.all()
    })


@csrf_protect
@decorator_from_middleware(middlewares.DashboardAuthenticate)
@decorator_from_middleware(middlewares.AdminAuthenticate)
def create(request):

    if request.method == "POST":

        params = request_params(request)
        validator = forms.CreateUserForm(params)

        if not validator.is_valid():
            messages.warning(request, "Something's wrrong!")
            return render(request, 'dashboard/users/add.html', {
                "page": "users",
                "roles": Role.objects.all(),
                'form': validator
            })

        new_user = User.objects.create_user(
            params["username"],
            params["email"],
            params["password"],
            fullname=params["fullname"],
            role_id=params["role"],
        )

        if new_user:
            messages.success(request, 'User created successfully!')
        else:
            messages.warning(request, "Something's wrrong!")

        return redirect("add_user_form")

    else:

        return render(request, 'dashboard/users/add.html', {
            "page": "users",
            "roles": Role.objects.all()
        })
