# Generated by Django 5.1.4 on 2025-01-06 05:13

import api.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0018_game_popularity_score'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='banner_image',
            field=models.ImageField(default=None, null=True, upload_to=api.models.format_banner_filename),
        ),
    ]
