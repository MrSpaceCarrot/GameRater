from django.urls import path
from .views import games, add_game, game, discord_callback, verifytoken

urlpatterns = [
    # Auth
    path('auth/verifytoken', verifytoken, name='verifytoken'),
    path('auth/discordcallback', discord_callback, name='discord_callback'),
    
    # Games
    path('games/', games, name='get_games'),
    path('games/add', add_game, name='add_game'),
    path('games/<int:pk>', game, name='game'),
]