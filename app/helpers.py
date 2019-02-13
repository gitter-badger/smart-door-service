import os
import jwt
import datetime
from flask import Flask
from django.conf import settings
from flask_bcrypt import Bcrypt


def request_params(request):
    params = {}
    for key in request.GET:
        params[key] = request.GET[key]

    for key in request.POST:
        params[key] = request.GET[key]

    return params


def create_token(user_id):
    token = jwt.encode(
        payload=get_jwt_payload(user_id),
        key=os.getenv("JWT_SECRET_KEY"),
        algorithm=os.getenv("JWT_ALGORITHM")
    )

    return str(token, 'utf-8')


def decode_token(token):
    return jwt.decode(
        trim(token),
        os.getenv("JWT_SECRET_KEY"),
        algorithm=os.getenv("JWT_ALGORITHM"),
        verify=False
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


def bcrypt():
    app = Flask(__name__)
    app.config['BCRYPT_LOG_ROUNDS'] = 12
    app.config['BCRYPT_HASH_IDENT'] = '2b'
    app.config['BCRYPT_HANDLE_LONG_PASSWORDS'] = False
    return Bcrypt(app)


def trim(string):
    return string.replace('"', '')
