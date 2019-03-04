from app import models, serializers
from app.http import middlewares, respond
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import decorator_from_middleware


@csrf_exempt
@decorator_from_middleware(middlewares.Authenticate)
@decorator_from_middleware(middlewares.RefreshToken)
def index(request):

    queryset = models.Log.objects.filter(user=request.user)\
        .order_by('created_at')
        
    serializer = serializers.LogSerializer(queryset, many=True)

    return respond.succeed(serializer.data)
