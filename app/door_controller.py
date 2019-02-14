import os
import json
import time
import datetime
# import RPi.GPIO as GPIO
from pytz import timezone
from . import respond, middlewares, models
from django.utils.decorators import decorator_from_middleware


# GPIO.setwarnings(False)
# GPIO.setmode(GPIO.BCM)


@decorator_from_middleware(middlewares.Authenticate)
@decorator_from_middleware(middlewares.DetectDevice)
def open_door(request):
    # GPIO.setup(4, GPIO.OUT)
    # GPIO.output(4, 0)
    time.sleep(.40)
    # GPIO.output(4, 1)

    log_type = models.LogType.objects.get_or_create(
        pin_id=4,
        icon="fa fa-door-open",
        property=1,
    )

    models.Log.objects.create(
        user_id=request.user.id,
        type_id=log_type[0].id,
        device_id=request.device.id
    )

    return respond.update_succeeded()
