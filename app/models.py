from .helpers import *
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager


class UserManager(BaseUserManager):
    use_in_migrations = False

    def _create_user(self, username, email, password, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        if not username:
            raise ValueError('The given username must be set')
        email = self.normalize_email(email)
        username = self.model.normalize_username(username)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email, password, **extra_fields):
        role = Role.objects.filter(title="user").get()
        extra_fields.setdefault('role_id', role.id)
        extra_fields.setdefault('avatar', "default.png")
        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email, password, **extra_fields):
        role = Role.objects.filter(title="admin").get()
        extra_fields.setdefault('role_id', role.id)

        if extra_fields.get('role_id') is not role.id:
            raise ValueError('Superuser must have admin role.')

        return self._create_user(username, email, password, **extra_fields)


class Role(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=80)

    class Meta:
        db_table = 'roles'


class User(AbstractBaseUser):
    username_validator = UnicodeUsernameValidator()
    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[username_validator],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )
    fullname = models.CharField(_('fullname'), max_length=30, blank=True)
    email = models.EmailField(_('email address'), blank=True)
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']
    avatar = models.CharField(max_length=80)
    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name='role')

    joined_at = models.DateTimeField(_('date joined'), default=timezone.now)
    updated_at = models.DateTimeField(_('date updated'), default=timezone.now)

    objects = UserManager()

    def is_admin(self):
        role = Role.objects.filter(title="admin").get()
        return self.role_id is role.id

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
