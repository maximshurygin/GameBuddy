# Generated by Django 5.1.1 on 2024-10-07 08:02

import autoslug.fields
import games.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BuddyRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(verbose_name='Описание')),
                ('status', models.CharField(choices=[('open', 'Актуально'), ('closed', 'Неактуально')], default='open', max_length=10, verbose_name='Статус')),
                ('slug', autoslug.fields.AutoSlugField(editable=False, populate_from=('game', 'nickname', 'created_at'), slugify=games.models.custom_slugify, verbose_name='Слаг')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
            ],
            options={
                'verbose_name': 'Заявка',
                'verbose_name_plural': 'Заявки',
            },
        ),
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='Название')),
                ('icon', models.ImageField(upload_to='game_icons/', verbose_name='Изображение')),
                ('genre', models.CharField(max_length=50, verbose_name='Жанр')),
                ('slug', autoslug.fields.AutoSlugField(editable=False, populate_from='name', slugify=games.models.custom_slugify, verbose_name='Слаг')),
                ('release_date', models.DateTimeField(verbose_name='Дата выхода')),
            ],
            options={
                'verbose_name': 'Игра',
                'verbose_name_plural': 'Игры',
            },
        ),
    ]
