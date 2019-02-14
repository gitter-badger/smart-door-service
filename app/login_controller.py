import jwt
from .models import *
from .helpers import *
from . import respond, middlewares, forms
from django.utils.decorators import decorator_from_middleware


@decorator_from_middleware(middlewares.PostRequest)
def create(request):

    params = request_params(request)

    form = forms.CreateAuthTokenForm(params)

    if not form.is_valid():
        return respond.validation_error(form.errors)

    user = User.objects.get(username=params['username'])
    if user.check_password(password=params['password']):
        token = create_token(user.id)
        return respond.succeed({
            "user": get_user_attributes(user),
            "token": token
        })

    return respond.unauthorized()


@decorator_from_middleware(middlewares.PostRequest)
@decorator_from_middleware(middlewares.Authenticate)
def refresh(request):

    jwt_token = request.META['HTTP_AUTHORIZATION'].replace("Bearer ", "")

    decode = decode_token(jwt_token)
    user = User.objects.get(id=decode['sub'])

    token = create_token(decode['sub'])
    return respond.succeed({"user": get_user_attributes(user), "token": token})
