from app import models
from app.helpers import *
from app.http import respond
from django.shortcuts import render
from django.shortcuts import redirect
from django.utils.deprecation import MiddlewareMixin


class AdminAuthenticate(MiddlewareMixin):

    @staticmethod
    def process_request(request):

        if not request.user.is_admin():
            return redirect('dashboard')


class DashboardAuthenticate(MiddlewareMixin):

    @staticmethod
    def process_request(request):
        if not request.user.is_authenticated:
            return redirect('login')


class HttpNotFoundExceptionMiddleware(MiddlewareMixin):

    @staticmethod
    def process_response(request, response):
        if response.status_code == 404:
            if str(request.path).startswith("/api"):
                return respond.not_found()

            return render(request, 'errors/404.html', status=404)

        if response.status_code == 403:
            return render(request, 'errors/403.html', status=404)

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


class CheckUserExistsWithToken(MiddlewareMixin):

    @staticmethod
    def process_request(request):

        if request.META.get("HTTP_AUTHORIZATION") is None:
            return respond.failed("Token is required!")

        try:

            token = request.META['HTTP_AUTHORIZATION'].replace("Bearer ", "")

            decode = jwt.decode(
                helpers.trim(token),
                os.getenv("JWT_SECRET_KEY"),
                algorithm=os.getenv("JWT_ALGORITHM"),
                verify=False
            )

            user = models.User.objects.filter(id=decode['sub'])

            if user.exists():
                request.user = user.get()
                return None

        except Exception or jwt.exceptions.DecodeError:
            return respond.unauthorized()

        return respond.unauthorized()


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


class DetectDevice(MiddlewareMixin):

    @staticmethod
    def process_request(request):
        device_os = "Unknown"
        device_model = "Unknown"
        device_type = "Unknown"
        device_icon = "fas fa-question"

        if request.META.get("HTTP_DEVICE") is not None:
            device_os = request.META.get("HTTP_DEVICE")

        if request.META.get("HTTP_MODEL") is not None:
            device_model = request.META.get("HTTP_MODEL")

        if request.META.get("HTTP_TYPE") is not None:
            device_type = request.META.get("HTTP_TYPE")

        if device_os == "iPhone":
            device_icon = "fas fa-mobile-alt"

        if device_os == "Android":
            device_icon = "fab fa-android"

        if device_os == "Terminal":
            device_icon = "fas fa-terminal"

        if device_os == "Linux":
            device_icon = "fab fa-linux"

        if device_os == "macOS":
            device_icon = "fab fa-apple"

        device = models.Device.objects.get_or_create(
            type=device_type,
            model=device_model,
            os=device_os,
            icon=device_icon
        )

        if device[0]:
            request.device = device[0]

        return None
