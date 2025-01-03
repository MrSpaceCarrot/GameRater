from django.db import models
from django.utils import timezone
from datetime import datetime, timedelta

# Add one week for tokens
def add_one_week():
    return timezone.now() + timedelta(weeks=1)

# Create your models here.

# Game model
class Game(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
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
    added_by = models.ForeignKey("DiscordUser", on_delete=models.SET_NULL, related_name="gamesadded", default=None, null=True)
    update_banner_link = models.BooleanField(default=True)
    average_rating = models.FloatField(default=None, null=True)

    def __str__(self):
        return self.name
    
# Game tag model
class Tag(models.Model):
    id =models.AutoField(primary_key=True, unique=True)
    tag = models.CharField(max_length=50, default=None)

    def __str__(self):
        return self.tag
    
# Rating model
class Rating(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    game = models.ForeignKey("Game", on_delete=models.CASCADE, related_name="ratings", default=None)
    user = models.ForeignKey("DiscordUser", on_delete=models.CASCADE, related_name="ratings", default=None)
    rating = models.SmallIntegerField(default=None)
    date_added = models.DateTimeField("Date added", default=timezone.now)

    def __str__(self):
        return self.id
    
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
    account_activated = models.BooleanField(default=False)
    can_add_games = models.BooleanField(default=False)

    def is_authenticated(self, request):
        return True
    
    def __str__(self):
        return self.username

# Auth Token Model
class AuthToken(models.Model):
    user = models.ForeignKey("DiscordUser", on_delete=models.CASCADE, related_name="tokens", default=None)
    token = models.CharField(max_length=255, unique=True)
    created = models.DateTimeField(auto_now_add=True)
    expiry_date = models.DateTimeField("Expiry Date", default=add_one_week)

    def __str__(self):
        return self.token