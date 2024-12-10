from django.urls import path
from .views import games, recentlyaddedgames, recentlyupdatedgames, add_game, game, discord_callback, tags, current_user

urlpatterns = [
    # Auth
    path('auth/discordcallback', discord_callback, name='discord_callback'),
    path('currentuser', current_user, name='current_user'),
    
    # Games
    path('games/', games, name='get_games'),
    path('games/recentadd', recentlyaddedgames, name='recentadd'),
    path('games/recentupdate', recentlyupdatedgames, name='recentupdate'),
    path('games/add', add_game, name='add_game'),
    path('games/<int:pk>', game, name='game'),
    path('tags/', tags, name='tags'),
]