import time
# import RPi.GPIO as GPIO
from app import models
from app.http import middlewares, respond
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import decorator_from_middleware
from django.views.decorators.http import require_POST


# GPIO.setwarnings(False)
# GPIO.setmode(GPIO.BCM)


@csrf_exempt
@require_POST
@decorator_from_middleware(middlewares.Authenticate)
@decorator_from_middleware(middlewares.DetectDevice)
def open_door(request):
    # GPIO.setup(4, GPIO.OUT)
    # GPIO.output(4, 0)
    time.sleep(.40)
    # GPIO.output(4, 1)

    accessory = models.Accessory.objects.filter(name="Door").get()

    models.Log.objects.create(
        user_id=request.user.id,
        accessory_id=accessory.id,
        device_id=request.device.id
    )

    return respond.succeed_message("The yard door opened successfully!")
