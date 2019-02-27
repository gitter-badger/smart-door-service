from .helpers import *
from django.db import models
from django.contrib.auth.models import User


class Device(models.Model):
    id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=80)
    os = models.CharField(max_length=80)
    model = models.CharField(max_length=80)
    icon = models.CharField(max_length=80)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'devices'


class LogType(models.Model):
    id = models.AutoField(primary_key=True)
    priority = models.CharField(max_length=80)
    pin_id = models.CharField(max_length=80)
    icon = models.CharField(max_length=80)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'log_types'


class Log(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    device = models.ForeignKey(Device, on_delete=None, related_name='device')
    type = models.ForeignKey(LogType, on_delete=None, related_name='type')
    created_at = models.DateTimeField(auto_now_add=True)
    readed = models.BooleanField(default=False)
    # updted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'logs'
