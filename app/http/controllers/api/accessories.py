import json
from app.http import respond
from app import models, serializers


def index(request):    
    accessories = models.Accessory.objects.all()
    serializer = serializers.AccesstorySerializer(accessories, many=True)

    return respond.succeed(serializer.data)