from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from accounts.manager import UserManager


# Create your models here.

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    phone_number = models.CharField(max_length=11, unique=True)
    full_name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    # field that use for authenticated
    USERNAME_FIELD = 'phone_number'
    # for superuser command
    REQUIRED_FIELDS = ['email', 'full_name']

    # manager
    objects = UserManager()

    def __str__(self):
        return self.email

    # staff : user allows to access to admin page
    @property
    def is_staff(self):
        return self.is_admin


class OtpCode(models.Model):
    phone_number = models.CharField(max_length=11, unique=True)
    code = models.PositiveSmallIntegerField()
    created_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.phone_number}-{self.code}-{self.created_time}'
