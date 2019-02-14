from django.db import models
from .helpers import *


class User(models.Model):
    id = models.AutoField(primary_key=True)
    fullname = models.CharField(max_length=80)
    username = models.CharField(max_length=30)
    email = models.CharField(max_length=30)
    password = models.CharField(max_length=128)
    avatar = models.CharField(max_length=80)
    role_id = models.CharField(max_length=80)
    verified = models.CharField(max_length=80)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def check_password(self, password):
        if not self.password or not password:
            return False
        return bcrypt().check_password_hash(self.password, password)

    class Meta:
        db_table = 'users'


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
