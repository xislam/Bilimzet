from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models


# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self, phone_number, name, password=None, **extra_fields):
        if not phone_number:
            raise ValueError('The Phone Number field must be set')
        user = self.model(phone_number=phone_number, name=name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, password, name, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(phone_number, password, name, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=20, verbose_name='ФИО', null=True, blank=True)
    phone_number = models.CharField(max_length=18, verbose_name='Телефон', null=False, blank=False, unique=True,
                                    error_messages={
                                        'unique': "Пользователь с указанным номером телефона уже существует.",
                                    }, )
    email = models.EmailField(verbose_name='Email', unique=True, null=True, blank=True)
    device_token = models.CharField(max_length=500, verbose_name='Токен устройства', null=True, blank=True)
    phone_number_verified = models.BooleanField(verbose_name="Верифицирован", default=False)
    verification_code = models.CharField(max_length=6, null=True, blank=True)
    receive_notifications = models.BooleanField(verbose_name="Получать уведомления", default=True, null=False,
                                                blank=True)
    avatar = models.ImageField(upload_to='avatar/', null=True, blank=True)
    receive_promotions = models.BooleanField(verbose_name="Получать акции", default=True, null=False, blank=True)
    receive_email_notifications = models.BooleanField(verbose_name="Получать уведомления по почте", default=True,
                                                      null=False, blank=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return str(f"{self.name} номер: {self.phone_number}")

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class VerificationCode(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='code')
    code = models.CharField(max_length=6)
    verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Verification code for {self.user.phone_number}"
