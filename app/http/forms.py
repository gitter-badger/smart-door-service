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


class CreateAuthTokenForm(forms.Form):
    username = forms.CharField(max_length=100, required=True, validators=[validate_exists])
    password = forms.CharField(max_length=100, required=True)
