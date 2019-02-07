import os
import json
import time
import datetime
import RPi.GPIO as GPIO
from pytz import timezone
from . import respond, middlewares, models
from django.utils.decorators import decorator_from_middleware

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)


@decorator_from_middleware(middlewares.AuthenticateMiddleware)
def open_door(request):
    GPIO.setup(4, GPIO.OUT)
    GPIO.output(4, 0)
    time.sleep(.40)
    GPIO.output(4, 1)

    log_type = models.LogType.objects.get(pin_id=4)

    user = models.Log.objects.create(
        user_id=request.user.id,
        type_id=log_type.id,
        device_id=request.GET['device_id']
    )
    return respond.update_succeeded()
