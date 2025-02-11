# Generated by Django 5.1.2 on 2024-12-21 08:05

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0011_rating'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rating',
            name='game',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='ratings', to='api.game'),
        ),
        migrations.AlterField(
            model_name='rating',
            name='user',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='ratings', to='api.discorduser'),
        ),
    ]
