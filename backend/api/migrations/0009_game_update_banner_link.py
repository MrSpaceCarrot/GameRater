# Generated by Django 5.1.2 on 2024-12-07 08:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_game_added_by'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='update_banner_link',
            field=models.BooleanField(default=True, null=True),
        ),
    ]
