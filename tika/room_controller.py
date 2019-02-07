import os
import redis
import json
import time
import datetime
import RPi.GPIO as GPIO
from pytz import timezone
from . import respond, middlewares
from django.utils.decorators import decorator_from_middleware

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

redis_client = redis.StrictRedis(host=os.getenv('REDIS_HOST'), port=os.getenv('REDIS_PORT'), db=os.getenv('REDIS_DB'))


@decorator_from_middleware(middlewares.AuthenticateMiddleware)
def lights(request):
    GPIO.setup(17, GPIO.OUT)
    if str(redis_client.get('lights'), "utf-8") == "0":
        GPIO.output(17, 1)
        redis_client.set('lights', "1")
    else:
        GPIO.output(17, 0)
        redis_client.set('lights', "0")

    return respond.update_succeeded()
