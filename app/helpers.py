import os
import jwt
import datetime
from app import models
from django.conf import settings


def request_params(request):
    params = {}
    for key in request.GET:
        params[key] = request.GET.get(key)

    for key in request.POST:
        params[key] = request.POST.get(key)

    return params


def create_token(user_id):
    token = jwt.encode(
        payload=get_jwt_payload(user_id),
        key=os.getenv("JWT_SECRET_KEY"),
        algorithm=os.getenv("JWT_ALGORITHM")
    )

    return str(token, 'utf-8')


def decode_token(token, verify_exp=True):
    return jwt.decode(
        trim(token),
        os.getenv("JWT_SECRET_KEY"),
        algorithm=os.getenv("JWT_ALGORITHM"),
        options={'verify_exp': verify_exp}
    )


def get_user_attributes(user):
    return {
        "id": user.id,
        "username": user.username,
        "fullname": user.fullname,
        "avatar": user.avatar if user.avatar is not None else "avatar.png"
    }


def get_jwt_payload(user_id):
    return {
        'sub': int(user_id),
        'iat': datetime.datetime.utcnow(),
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=int(os.getenv('JWT_EXP'))),
    }


def trim(string):
    return string.replace('"', '')
