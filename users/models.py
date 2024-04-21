from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator, MaxLengthValidator


# Create your models here.

class User(AbstractUser):
    """Модель пользователя"""
    username = None
    name = models.CharField(blank=True, null=True, validators=[
        RegexValidator(
            regex=r'^[а-яА-Яa-zA-Z\s]*$',
            message='Некорректные символы. Используйте только кириллицу, латиницу, пробел.',
            code='invalid_name',
        ),
        MaxLengthValidator(100, message='Длина не должна превышать 100 символов.')
    ],
                            verbose_name='Имя')
    surname = models.CharField(blank=True, null=True, validators=[
        RegexValidator(
            regex=r'^[а-яА-Яa-zA-Z\s]*$',
            message='Некорректные символы. Используйте кириллицу, латиницу, пробел.',
            code='invalid_surname',
        ),
        MaxLengthValidator(100, message='Длина не должна превышать 100 символов.')
    ],
                               verbose_name='Отчество')
    family = models.CharField(blank=True, null=True, validators=[
        RegexValidator(
            regex=r'^[а-яА-Яa-zA-Z\s]*$',
            message='Некорректные символы. Используйте только кириллицу, латиницу, пробел.',
            code='invalid_family',
        ),
        MaxLengthValidator(100, message='Длина не должна превышать 100 символов.')
    ],
                              verbose_name='Фамилия')
    email = models.EmailField(unique=True, verbose_name='Электронная почта')
    phone = models.CharField(blank=True, null=True, validators=[
        RegexValidator(
            regex=r'^[0-9+]*$',
            message='Некорректный номер телефона.',
            code='invalid_phone',
        ),
        MaxLengthValidator(18, message='Длина не должна превышать 18 символов.')
    ],
                             verbose_name='Номер телефона')
    is_boss = models.BooleanField(default=False, null=True, verbose_name='Руководитель')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return f"{self.name} {self.surname} {self.family}"

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователя'
