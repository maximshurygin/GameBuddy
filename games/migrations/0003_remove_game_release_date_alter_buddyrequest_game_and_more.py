# Generated by Django 5.1.1 on 2024-10-07 09:37

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0002_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='game',
            name='release_date',
        ),
        migrations.AlterField(
            model_name='buddyrequest',
            name='game',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='buddy_requests', to='games.game', verbose_name='Игра'),
        ),
        migrations.AlterField(
            model_name='buddyrequest',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='buddy_requests', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
        ),
    ]
