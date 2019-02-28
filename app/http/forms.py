from django import forms
from app.models import *
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy


def validate_exists(value):
    user = User.objects.filter(username=value)

    if not user.exists():
        raise ValidationError(
            gettext_lazy('User %(username)s does not exists!'),
            params={'username': value},
        )


def validate_unique_username(value):
    user = User.objects.filter(username=value)

    if user.exists():
        raise ValidationError(
            gettext_lazy('Username %(username)s already exists!'),
            params={'username': value},
        )


def validate_unique_email(value):
    user = User.objects.filter(email=value)

    if user.exists():
        raise ValidationError(
            gettext_lazy('Email %(email)s already exists!'),
            params={'email': value},
        )


class CreateAuthTokenForm(forms.Form):
    username = forms.CharField(max_length=100, required=True, validators=[validate_exists])
    password = forms.CharField(max_length=100, required=True)


class CreateUserForm(forms.Form):
    fullname = forms.CharField(max_length=100, required=True)
    username = forms.CharField(max_length=100, required=True, validators=[validate_unique_username])
    password = forms.CharField(max_length=100, required=True)
    password_confirmation = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(max_length=100, required=True, validators=[validate_unique_email])
    role = forms.ChoiceField(widget=forms.Select, choices=(('1', 'Admin'), ('2', 'User')))
