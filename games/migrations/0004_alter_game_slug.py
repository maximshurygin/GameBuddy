# Generated by Django 5.1.1 on 2024-10-07 09:39

import autoslug.fields
import games.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0003_remove_game_release_date_alter_buddyrequest_game_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='slug',
            field=autoslug.fields.AutoSlugField(editable=False, populate_from='title', slugify=games.models.custom_slugify, verbose_name='Слаг'),
        ),
    ]
