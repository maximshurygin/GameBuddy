from django.contrib.auth import get_user_model
from django.db import models
from autoslug import AutoSlugField
from django.urls import reverse
from multiselectfield import MultiSelectField
from unidecode import unidecode
from django.utils.text import slugify

# Create your models here.

NULLABLE = {'null': True, 'blank': True}


def custom_slugify(value):
    return slugify(unidecode(value))


class Game(models.Model):
    title = models.CharField(max_length=100, verbose_name='Название')
    icon = models.ImageField(upload_to='game_icons/', verbose_name='Изображение')
    slug = AutoSlugField(populate_from='title', slugify=custom_slugify, verbose_name='Слаг')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('games:game_detail', args=[str(self.slug)])

    class Meta:
        verbose_name = 'Игра'
        verbose_name_plural = 'Игры'


class BuddyRequest(models.Model):
    STATUS_CHOICES = [
        ('open', 'Актуально'),
        ('closed', 'Неактуально')
    ]
    VOICE_CHOICES = (
        ('RaidCall', 'RaidCall'),
        ('Discord', 'Discord'),
        ('TeamSpeak', 'TeamSpeak'),
        ('Skype', 'Skype'),
        ('Ventrillo', 'Ventrillo'),
    )
    GOAL_CHOICES = (
        ('pro', 'про'),
        ('fun', 'фан')
    )
    game = models.ForeignKey('Game', on_delete=models.CASCADE, related_name='buddy_requests', verbose_name='Игра')
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='buddy_requests',
                             verbose_name='Пользователь')
    description = models.TextField(verbose_name='Описание')
    min_age = models.PositiveIntegerField(**NULLABLE, verbose_name='Возраст от')
    max_age = models.PositiveIntegerField(**NULLABLE, verbose_name='Возраст до')
    goal = models.CharField(max_length=10, choices=GOAL_CHOICES, default='fun', verbose_name='Цель')
    voice = MultiSelectField(
        choices=VOICE_CHOICES,
        max_length=200,
        **NULLABLE,
        verbose_name='Голосовые чаты'
    )
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='open', verbose_name='Статус')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    def __str__(self):
        return f'{self.user.nickname} - {self.game.title} - {self.status}'

    def get_absolute_url(self):
        return reverse('games:game_detail', args=[str(self.pk)])

    class Meta:
        verbose_name = 'Заявка'
        verbose_name_plural = 'Заявки'
