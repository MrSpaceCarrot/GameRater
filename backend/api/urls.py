from django.urls import path
from .views import games, add_game, game

urlpatterns = [
    path('games/', games, name='get_games'),
    path('games/add', add_game, name='add_game'),
    path('games/<int:pk>', game, name='game')
]