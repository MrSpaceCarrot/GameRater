from typing import Any
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils import timezone
from django.http import HttpRequest
from .models import DiscordUser, AuthToken
import requests
import uuid
from decouple import config
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

# Discord authentication custom backend
class DiscordAuthBackend(BaseBackend):
    def authenticate(self, request, access_code) -> DiscordUser:
        # Get user info and set variables
        access_token = get_discord_access_token(access_code)
        user_info = get_discord_user_info(access_token)
        discord_id = str(user_info["id"])
        avatar_link = f"https://cdn.discordapp.com/avatars/{user_info['id']}/{user_info['avatar']}?size=1024"
    
        # Get or create user
        user, created = DiscordUser.objects.get_or_create(
            discord_id=discord_id,
            defaults={
                'username': user_info['username'],
                'avatar_link': avatar_link,
                'last_login': timezone.now(),
                'display_name': user_info['username'],
            },
        )
        if not created:
            user.last_login = timezone.now()
            user.save()

        # Get token for user
        token, _ = AuthToken.objects.get_or_create(user=user)
        if not token.token:
            token.token = str(uuid.uuid4())
            token.save()

        # Return user and token
        return user, token.token

    # Return a specific user
    def get_user(self, user_id):
        try:
            return DiscordUser.objects.get(pk=user_id)
        except DiscordUser.DoesNotExist:
            return None
        

# Discord token authentication
class DiscordTokenAuthentication(BaseAuthentication):
    def authenticate(self, request):
        token = request.headers.get('Authorization')
        if not token:
            return None

        token = token.split(' ')[-1]
        try:
            discord_token = AuthToken.objects.get(token=token)
        except AuthToken.DoesNotExist:
            raise AuthenticationFailed("Invalid token")

        return (discord_token.user, None)


def get_discord_access_token(access_code):
    token_url = "https://discord.com/api/oauth2/token"
    data = {
        "client_id": config("DISCORD_CLIENT_ID"),
        "client_secret": config("DISCORD_CLIENT_SECRET"),
        "grant_type": "authorization_code",
        "code": access_code,
        "redirect_uri": config("FINAL_REDIRECT_URI"),
        "scope": "identify"
    }
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    response = requests.post(token_url, data=data, headers=headers)
    if response.status_code != 200:
        print("Error fetching access token:", response.json())
        return None
    return response.json().get('access_token')


def get_discord_user_info(access_token):
    headers = {'Authorization': f"Bearer {access_token}"}
    response = requests.get("https://discord.com/api/v10/users/@me", headers=headers).json()
    return response