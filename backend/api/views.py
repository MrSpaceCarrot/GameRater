from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from .models import Game, Tag, Rating
from .serializer import GameSerializer, TagSerializer, DiscordUserSerializer, RatingSerializer
from .services import GameService, get_user_from_auth_header
from .auth import DiscordAuthBackend, DiscordTokenAuthentication
from django_ratelimit.decorators import ratelimit

# Endpoints

# Games
# Get all games (name)
@api_view(["GET"])
@authentication_classes([DiscordTokenAuthentication])
@permission_classes([IsAuthenticated])
@ratelimit(key='ip', rate='100/m', block=True)
def games(request):
    games = Game.objects.all().order_by('name')
    serializer = GameSerializer(games, many=True)
    return Response(serializer.data)

# Get 6 most recently added games
@api_view(["GET"])
@authentication_classes([DiscordTokenAuthentication])
@permission_classes([IsAuthenticated])
@ratelimit(key='ip', rate='100/m', block=True)
def recentlyaddedgames(request):
    games = Game.objects.all().order_by('-date_added')[:6]
    serializer = GameSerializer(games, many=True)
    return Response(serializer.data)

# Get 6 most recently updated games
@api_view(["GET"])
@authentication_classes([DiscordTokenAuthentication])
@permission_classes([IsAuthenticated])
@ratelimit(key='ip', rate='100/m', block=True)
def recentlyupdatedgames(request):
    games = Game.objects.filter(last_updated__isnull=False).order_by('-last_updated')[:6]
    serializer = GameSerializer(games, many=True)
    return Response(serializer.data)

# Get 6 games which have not recieved updates the longest
@api_view(["GET"])
@authentication_classes([DiscordTokenAuthentication])
@permission_classes([IsAuthenticated])
@ratelimit(key='ip', rate='100/m', block=True)
def deadgames(request):
    games = Game.objects.filter(last_updated__isnull=False).order_by('last_updated')[:6]
    serializer = GameSerializer(games, many=True)
    return Response(serializer.data)

# Get 6 random games
@api_view(["GET"])
@authentication_classes([DiscordTokenAuthentication])
@permission_classes([IsAuthenticated])
@ratelimit(key='ip', rate='100/m', block=True)
def randomgames(request):
    games = Game.objects.all().order_by('?')[:6]
    serializer = GameSerializer(games, many=True)
    return Response(serializer.data)

# Get 6 highest rated games
@api_view(["GET"])
@authentication_classes([DiscordTokenAuthentication])
@permission_classes([IsAuthenticated])
@ratelimit(key='ip', rate='100/m', block=True)
def topgames(request):
    games = Game.objects.all().order_by('-average_rating')[:6]
    serializer = GameSerializer(games, many=True)
    return Response(serializer.data)

# Get game tags list
@api_view(["GET"])
@authentication_classes([DiscordTokenAuthentication])
@permission_classes([IsAuthenticated])
@ratelimit(key='ip', rate='100/m', block=True)
def tags(request):
    tags = Tag.objects.all().order_by('tag')
    serializer = TagSerializer(tags, many=True)
    return Response(serializer.data)

# Add game
@api_view(["POST"])
@authentication_classes([DiscordTokenAuthentication])
@permission_classes([IsAuthenticated])
@ratelimit(key='ip', rate='100/m', block=True)
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
@ratelimit(key='ip', rate='100/m', block=True)
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
        serializer = GameSerializer(game, data=request.data, context=request.headers['Authorization'], partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # Delete game
    elif request.method == "DELETE":
        # Check permissions
        game_added_by = game.added_by
        user_object = get_user_from_auth_header(request.headers.get('Authorization'))
        if user_object.id != game_added_by.id:
            return Response({"error": "You do not have permission to delete this resource"}, status=status.HTTP_401_UNAUTHORIZED)

        game.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# Ratings
# Rate game
@api_view(["POST"])
@authentication_classes([DiscordTokenAuthentication])
@permission_classes([IsAuthenticated])
@ratelimit(key='ip', rate='100/m', block=True)
def add_rating(request):
    serializer = RatingSerializer(data=request.data, context=request.headers['Authorization'])
    if serializer.is_valid():
        rating = serializer.save()
        service = GameService()
        print(rating.game_id)
        service.update_average_rating(rating.game_id)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Get current user's ratings
@api_view(["GET"])
@authentication_classes([DiscordTokenAuthentication])
@permission_classes([IsAuthenticated])
@ratelimit(key='ip', rate='100/m', block=True)
def user_ratings(request):
    games = Rating.objects.filter(user=get_user_from_auth_header(request.headers.get('Authorization')))
    serializer = RatingSerializer(games, many=True)
    return Response(serializer.data)


# Authentication & Users
# Discord login
@api_view(['POST'])
@ratelimit(key='ip', rate='10/m', block=True)
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
@api_view(["GET"])
@authentication_classes([DiscordTokenAuthentication])
@permission_classes([IsAuthenticated])
@ratelimit(key='ip', rate='100/m', block=True)
def current_user(request):
    # Get current user's token
    user_object = get_user_from_auth_header(request.headers.get('Authorization'))
    
    # Return object
    serializer = DiscordUserSerializer(user_object)
    return Response(serializer.data)

