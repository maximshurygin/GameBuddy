from django.contrib.auth.models import AbstractUser
from django.db import models
from django_countries.fields import CountryField

NULLABLE = {'null': True, 'blank': True}


class User(AbstractUser):
    GENDER_CHOICES = (
        ('male', 'Мужской'),
        ('female', 'Женский'),
    )

    username = None

    email = models.EmailField(
        unique=True,
        verbose_name='Email'
    )

    nickname = models.CharField(
        max_length=100,
        verbose_name='Ник'
    )

    gender = models.CharField(
        max_length=10,
        choices=GENDER_CHOICES,
        **NULLABLE,
        verbose_name='Пол'
    )

    age = models.PositiveIntegerField(
        **NULLABLE,
        verbose_name='Возраст'
    )

    country = CountryField(
        **NULLABLE,
        verbose_name='Страна'
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['nickname']

    def __str__(self):
        return self.email
