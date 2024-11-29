from django.db import models
from django.utils import timezone

# Create your models here.

# Game model
class Game(models.Model):
    id =models.AutoField(primary_key=True, unique=True)
    name = models.CharField(max_length=100, default=None)
    platform = models.CharField(max_length=10, default=None)
    install_size = models.SmallIntegerField(default=None, null=True)
    link = models.CharField(max_length=300, default=None)
    banner_link = models.CharField(max_length=300, default=None)
    min_party_size = models.SmallIntegerField(default=None)
    max_party_size = models.SmallIntegerField(default=None)
    tags = models.CharField(max_length=300, default=None)
    last_updated = models.DateTimeField("Last Updated", default=None, null=True)
    date_added = models.DateTimeField("Date added", default=timezone.now)

    def __str__(self):
        return self.name