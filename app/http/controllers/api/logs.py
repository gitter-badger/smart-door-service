from app.models import *
from app.http import middlewares, respond
from django.utils.decorators import decorator_from_middleware


@decorator_from_middleware(middlewares.Authenticate)
@decorator_from_middleware(middlewares.RefreshToken)
def index(request):
    logs = Log.objects.filter(user=request.user)\
        .order_by('created_at')\

    return respond.succeed(respond.model_datas(logs))