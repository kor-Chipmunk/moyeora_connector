from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from .managers import UserManager

class User(AbstractBaseUser, PermissionsMixin):
    objects = UserManager()

    email = models.EmailField(verbose_name='이메일', max_length=255, unique=True)
    nickname = models.CharField(verbose_name='닉네임', max_length=20, null=False, unique=True)
    created_at = models.DateTimeField(verbose_name='생성 일자', auto_now_add=True)

    is_active = models.BooleanField(verbose_name='활성 유저 여부', default=True)
    is_staff = models.BooleanField(verbose_name='스태프 여부', default=False)
    is_admin = models.BooleanField(verbose_name='관리자 여부', default=False)
    is_superuser = models.BooleanField(verbose_name='총 관리자 여부', default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nickname']

    def __str__(self):
        nickname = self.nickname
        if nickname == "":
            return self.email
        else:
            return self.nickname

    class Meta:
        verbose_name = '고객'
        verbose_name_plural = f'{verbose_name} 목록'
        ordering = ('-created_at', )