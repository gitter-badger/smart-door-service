import os
import jwt
from .helpers import *
from django.utils.deprecation import MiddlewareMixin
from . import respond, helpers, models


class HttpNotFoundExceptionMiddleware(MiddlewareMixin):

    @staticmethod
    def process_response(request, response):
        if response.status_code == 404:
            return respond.not_found()

        return response


class PostRequest(MiddlewareMixin):

    @staticmethod
    def process_request(request):

        if request.method != "POST":
            return respond.method_not_allowed()

        return None


class RefreshToken(MiddlewareMixin):

    @staticmethod
    def process_response(request, response):

        if request.META.get("HTTP_AUTHORIZATION") is not None:

            jwt_token = request.META['HTTP_AUTHORIZATION'].replace("Bearer ", "")
            decode = decode_token(jwt_token)
            token = create_token(decode['sub'])
            response["Authorization"] = token

        return response


class Authenticate(MiddlewareMixin):

    @staticmethod
    def process_request(request):

        if request.META.get("HTTP_AUTHORIZATION") is None:
            return respond.failed("Token is required!")

        try:

            token = request.META['HTTP_AUTHORIZATION'].replace("Bearer ", "")

            decode = jwt.decode(
                helpers.trim(token),
                os.getenv("JWT_SECRET_KEY"),
                algorithm=os.getenv("JWT_ALGORITHM")
            )

            user = models.User.objects.filter(id=decode['sub'])

            if user.exists():
                request.user = user.get()
                return None

        except Exception or jwt.exceptions.ExpiredSignature:
            return respond.unauthorized()

        return respond.unauthorized()
