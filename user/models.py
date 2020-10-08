from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from .managers import UserManager

class User(AbstractBaseUser, PermissionsMixin):
    objects = UserManager()

    email = models.EmailField(max_length=255, unique=True)
    nickname = models.CharField(max_length=20, null=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nickname']

    def __str__(self):
        nickname = self.nickname
        if nickname == "":
            return self.email
        else:
            return self.nickname

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'
        ordering = ('-created_at', )