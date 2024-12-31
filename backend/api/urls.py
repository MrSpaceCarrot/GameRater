from django.urls import path
from .views import *

urlpatterns = [
    # Auth
    path('auth/discordcallback', discord_callback, name='discord_callback'),
    path('auth/logout', logout, name='logout'),
    path('auth/logoutall', logoutall, name='logoutall'),

    # Users
    path('users/currentuser', current_user, name='current_user'),
    path('users/', users, name='users'),
    path('users/<int:pk>', user, name='user'),
    
    # Games
    path('games/', games, name='get_games'),
    path('games/recentadd', recentlyaddedgames, name='recentadd'),
    path('games/recentupdate', recentlyupdatedgames, name='recentupdate'),
    path('games/dead', deadgames, name='dead'),
    path('games/random', randomgames, name='random'),
    path('games/top', topgames, name='top'),
    path('games/add', add_game, name='add_game'),
    path('games/<int:pk>', game, name='game'),
    path('games/tags/', tags, name='tags'),

    # Ratings
    path('ratings/add/', add_rating, name='add_rating'),
    path('ratings/user/', user_ratings, name='user_ratings'),
]