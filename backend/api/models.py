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
    tags = models.JSONField(default=None)
    last_updated = models.DateTimeField("Last Updated", default=None, null=True)
    date_added = models.DateTimeField("Date added", default=timezone.now)
    added_by = models.ForeignKey("DiscordUser", on_delete=models.SET_NULL, related_name="gamesadded" ,default=None, null=True)
    update_banner_link = models.BooleanField(default=True)

    def __str__(self):
        return self.name
    
# Game tag model
class Tag(models.Model):
    id =models.AutoField(primary_key=True, unique=True)
    tag = models.CharField(max_length=50, default=None)

    def __str__(self):
        return self.tag
    
# Discord User Model
class DiscordUser(models.Model):
    id = models.AutoField(primary_key=True)
    discord_id = models.CharField(max_length=100, default=None)
    username = models.CharField(max_length=100)
    avatar_link = models.CharField(max_length=100, default=None)
    first_login = models.DateTimeField("First Login", default=timezone.now)
    last_login = models.DateTimeField(default=None, null=True)
    display_name = models.CharField(max_length=100, default=None)
    display_name_last_changed = models.DateTimeField(default=None, null=True)

    def is_authenticated(self, request):
        return True
    
    def __str__(self):
        return self.username

# Auth Token Model
class AuthToken(models.Model):
    user = models.OneToOneField('DiscordUser', on_delete=models.CASCADE)
    token = models.CharField(max_length=255, unique=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.token