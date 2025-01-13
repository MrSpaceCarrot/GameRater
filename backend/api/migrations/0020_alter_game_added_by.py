# Generated by Django 5.1.4 on 2025-01-06 21:48

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0019_game_banner_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='added_by',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='gamesadded', to='api.discorduser'),
        ),
    ]