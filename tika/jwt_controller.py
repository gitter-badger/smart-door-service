import os
import jwt
import bcrypt
import datetime
from . import respond, models, helpers, middlewares


def get_payload(user_id):
    return {
        'sub': int(user_id),
        'iat': datetime.datetime.utcnow(),
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=int(os.getenv('JWT_EXP'))),
    }


def create_token(user_id):
    token = jwt.encode(
        get_payload(user_id),
        os.getenv("JWT_SECRET_KEY"),
        algorithm=os.getenv("JWT_ALGORITHM")
    )

    return "Bearer " + str(token, 'utf-8')


def get_user(user):
    return {
        "id": user.id,
        "username": user.username,
        "fullname": user.fullname,
        "avatar": user.avatar if user.avatar is not None else "avatar.png"
    }


def create(request):
    user = models.User.objects.get(username=request.GET['username'])

    if bcrypt.checkpw(request.GET['password'].encode('utf8'), user.password.encode('utf8')):
        token = create_token(user.id)
        return respond.succeed({"user": get_user(user), "token": token})

    return respond.unauthorized()


def refresh(request):
    hash_token = request.META['HTTP_AUTHORIZATION'].replace("Bearer ", "")

    decode = jwt.decode(
        helpers.trim(hash_token),
        os.getenv("JWT_SECRET_KEY"),
        algorithm=os.getenv("JWT_ALGORITHM"),
        verify=False
    )

    user = models.User.objects.get(id=decode['sub'])

    token = create_token(decode['sub'])
    return respond.succeed({"user": get_user(user), "token": token})
