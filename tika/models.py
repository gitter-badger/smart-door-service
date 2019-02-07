from django.db import models


class User(models.Model):
    fullname = models.CharField(max_length=80)
    username = models.CharField(max_length=30)
    email = models.CharField(max_length=30)
    password = models.CharField(max_length=128)
    avatar = models.CharField(max_length=80)
    role_id = models.CharField(max_length=80)
    verified = models.CharField(max_length=80)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'users'


class LogType(models.Model):
    priority = models.CharField(max_length=80)
    pin_id = models.CharField(max_length=80)
    icon = models.CharField(max_length=80)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'log_types'


class Log(models.Model):
    user_id = models.CharField(max_length=80)
    type_id = models.CharField(max_length=80)
    device_id = models.CharField(max_length=80)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'logs'


class Device(models.Model):
    type = models.CharField(max_length=80)
    os = models.CharField(max_length=80)
    model = models.CharField(max_length=80)
    icon = models.CharField(max_length=80)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'devices'
