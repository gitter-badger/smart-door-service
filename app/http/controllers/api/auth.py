from app import helpers, serializers, models
from app.http import middlewares, respond, forms
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.utils.decorators import decorator_from_middleware


@csrf_exempt
@require_POST
def create(request):

    params = helpers.request_params(request)

    form = forms.CreateAuthTokenForm(params)

    if not form.is_valid():
        return respond.validation_error(form.errors)

    user = models.User.objects.get(username=params['username'])

    if user.check_password(params['password']):
        return respond.succeed({
            "user": serializers.UserSerializer(user).data,
            "token": helpers.create_token(user.id)
        })

    return respond.unauthorized()


@csrf_exempt
@require_POST
@decorator_from_middleware(middlewares.CheckUserExistsWithToken)
def refresh(request):

    jwt_token = request.META['HTTP_AUTHORIZATION'].replace("Bearer ", "")

    decode = helpers.decode_token(jwt_token, False)
    user = models.User.objects.get(id=decode['sub'])

    return respond.succeed({
        "user": serializers.UserSerializer(user).data, 
        "token": helpers.create_token(decode['sub'])
    })
