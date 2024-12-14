from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from .models import Game, Tag, AuthToken, DiscordUser
from .serializer import GameSerializer, TagSerializer, DiscordUserSerializer
from .services import GameService
from .auth import DiscordAuthBackend, DiscordTokenAuthentication

# Endpoints

# Games
# Get all games (name)
@api_view(["GET"])
@authentication_classes([DiscordTokenAuthentication])
@permission_classes([IsAuthenticated])
def games(request):
    games = Game.objects.all().order_by('name')
    serializer = GameSerializer(games, many=True)
    return Response(serializer.data)

# Get 6 most recently added games
@api_view(["GET"])
@authentication_classes([DiscordTokenAuthentication])
@permission_classes([IsAuthenticated])
def recentlyaddedgames(request):
    games = Game.objects.all().order_by('-date_added')[:6]
    serializer = GameSerializer(games, many=True)
    return Response(serializer.data)

# Get 6 most recently updated games
@api_view(["GET"])
@authentication_classes([DiscordTokenAuthentication])
@permission_classes([IsAuthenticated])
def recentlyupdatedgames(request):
    games = Game.objects.filter(last_updated__isnull=False).order_by('-last_updated')[:6]
    serializer = GameSerializer(games, many=True)
    return Response(serializer.data)

# Get 6 games which have not recieved updates the longest
@api_view(["GET"])
@authentication_classes([DiscordTokenAuthentication])
@permission_classes([IsAuthenticated])
def deadgames(request):
    games = Game.objects.filter(last_updated__isnull=False).order_by('last_updated')[:6]
    serializer = GameSerializer(games, many=True)
    return Response(serializer.data)

# Get game tags list
@api_view(["GET"])
@authentication_classes([DiscordTokenAuthentication])
@permission_classes([IsAuthenticated])
def tags(request):
    tags = Tag.objects.all().order_by('tag')
    serializer = TagSerializer(tags, many=True)
    return Response(serializer.data)

# Add game
@api_view(["POST"])
@authentication_classes([DiscordTokenAuthentication])
@permission_classes([IsAuthenticated])
def add_game(request):
    serializer = GameSerializer(data=request.data, context=request.headers['Authorization'])
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Specific game
@api_view(["GET", "PATCH", "DELETE"])
@authentication_classes([DiscordTokenAuthentication])
@permission_classes([IsAuthenticated])
def game(request, pk):
    # Check that game exists
    try:
        game = Game.objects.get(pk=pk)
    except Game.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    # Get game
    if request.method == "GET":
        serializer = GameSerializer(game)
        return Response(serializer.data)
    
    # Update game
    elif request.method == "PATCH":
        serializer = GameSerializer(game, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # Delete game
    elif request.method == "DELETE":
        game.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# Authentication & Users
# Discord login
@api_view(['POST'])
def discord_callback(request):
    access_code = request.data.get('access_code')
    if not access_code:
        return Response({"error": "Access code is missing"}, status=status.HTTP_400_BAD_REQUEST)

    auth_backend = DiscordAuthBackend()
    user, token = auth_backend.authenticate(request, access_code)

    if user is None:
        return Response({"error": "Authentication failed"}, status=status.HTTP_401_UNAUTHORIZED)

    return Response({
        "token": token,
        "username": user.username,
        "display_name": user.display_name,
        "avatar_link": user.avatar_link
    })

# Get currently logged in user
@api_view(["GET", "PATCH", "DELETE"])
@authentication_classes([DiscordTokenAuthentication])
@permission_classes([IsAuthenticated])
def current_user(request):
    # Get current user's token
    token = request.headers.get('Authorization').split(' ')[1]
    token_object = AuthToken.objects.get(token=token)
    user_object = DiscordUser.objects.get(id=token_object.user_id)
    
    # Return object
    serializer = DiscordUserSerializer(user_object)
    return Response(serializer.data)

