import os
import jwt
from django.utils.deprecation import MiddlewareMixin
from . import respond, helpers, models


class HttpNotFoundExceptionMiddleware(MiddlewareMixin):

    @staticmethod
    def process_response(request, response):
        if response.status_code == 404:
            return respond.not_found()

        return response


class AuthenticateMiddleware(MiddlewareMixin):

    @staticmethod
    def process_response(request, response):
        return response

    @staticmethod
    def process_request(request):

        try:

            hash_token = request.META['HTTP_AUTHORIZATION'].replace("Bearer ", "")

            decode = jwt.decode(
                helpers.trim(hash_token),
                os.getenv("JWT_SECRET_KEY"),
                algorithm=os.getenv("JWT_ALGORITHM")
            )

            user = models.User.objects.get(id=decode['sub'])

            if user:
                request.user = user
                return None

        except Exception or jwt.exceptions.ExpiredSignature:
            return respond.unauthorized()

        return respond.unauthorized()
