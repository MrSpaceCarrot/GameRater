from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from .models import Game, Tag
from .serializer import GameSerializer, TagSerializer
from .services import GameService
from .auth import DiscordAuthBackend, DiscordTokenAuthentication

# Endpoints

# Games
# Get all games
@api_view(["GET"])
@authentication_classes([DiscordTokenAuthentication])
@permission_classes([IsAuthenticated])
def games(request):
    games = Game.objects.all().order_by('name')
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
#@authentication_classes([DiscordTokenAuthentication])
#@permission_classes([IsAuthenticated])
def add_game(request):
    # Handle setting the banner link
    name = request.data.get("name", None)
    platform = request.data.get("platform", None)
    install_size = request.data.get("install_size", None)
    link = request.data.get("link", None)
    banner_link = request.data.get("banner_link", None)
    min_party_size = request.data.get("min_party_size", None)
    max_party_size = request.data.get("max_party_size", None)
    tags = request.data.get("tags", None)

    # Duplicate games check
    games = Game.objects.all().order_by('name')
    for game in games:
        if game.name == name or game.link == link:
            return Response({"detail": "This game has already been added"},status=status.HTTP_400_BAD_REQUEST)

    # Ensure platform is valid
    if platform not in ["Roblox", "Steam", "Party", "Other"]:
        return Response({"detail": "Invalid platform, games must be either Roblox, Steam, Party, or Other"},status=status.HTTP_400_BAD_REQUEST)
    
    #if platform == "Steam" and not type(install_size) == int:
    #    return Response({"detail": "Steam games must include an install_size"},status=status.HTTP_400_BAD_REQUEST)
    
    # If game is Party or Other, banner_link is required
    if platform in ["Party", "Other"] and not banner_link:
        return Response({"detail": f"{platform} games require a banner_link to be provided"},status=status.HTTP_400_BAD_REQUEST)

    # If game is Roblox or Steam, banner_link needs to be retrived
    if platform in ["Roblox", "Steam"]:
        # Get service
        game_service = GameService()

        # Get banner link
        banner_link = game_service.get_banner_link(platform, link)
        if not banner_link:
            return Response({"detail": "An error occured getting the banner link. The game link may be invalid."}, status=status.HTTP_400_BAD_REQUEST)

    # If game is Roblox, last_updated needs to be retrived
    if platform == "Roblox":
        last_updated = game_service.get_last_updated(platform, link)
        if not last_updated:
            return Response({"detail": "An error occured getting last updated. The game link may be invalid."}, status=status.HTTP_400_BAD_REQUEST)
    else:
        last_updated = None

    # Check that party size is valid
    if type(min_party_size) != int or type(max_party_size) != int or min_party_size < 2 or max_party_size > 16:
        return Response({"detail": "Party size range must be between 2 and 16"}, status=status.HTTP_400_BAD_REQUEST)

    # Alphabetically sort tags and check number
    if type(tags) != list or len(tags) < 2 or len(tags) > 5:
        return Response({"detail": "Please choose between 2 and 5 tags"}, status=status.HTTP_400_BAD_REQUEST)
    tags = sorted(tags)

    request.data["banner_link"] = banner_link
    request.data["last_updated"] = last_updated
    request.data["tags"] = tags
        
    # Serialize data
    serializer = GameSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    # Handle invalid data
    return Response(
        {
            "detail": "Invalid data",
            "errors": serializer.errors
        },
        status=status.HTTP_400_BAD_REQUEST
    )

# Specific game
@api_view(["GET", "PATCH", "DELETE"])
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

# Authentication
# Check if current token is valid
@api_view(["GET"])
@authentication_classes([DiscordTokenAuthentication])
@permission_classes([IsAuthenticated])
def verifytoken(request):
    return Response(status=status.HTTP_200_OK)

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
        "user_info": {
            "username": user.username,
            "discord_id": user.discord_id,
            "avatar_link": user.avatar_link
        },
        "token": token
    })
