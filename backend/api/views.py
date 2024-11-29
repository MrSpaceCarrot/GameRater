from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Game
from .serializer import GameSerializer
from .services import GameService

# Endpoints

# Get all games
@api_view(["GET"])
def games(request):
    games = Game.objects.all()
    serializer = GameSerializer(games, many=True)
    return Response(serializer.data)

# Add game
@api_view(["POST"])
def add_game(request):
    # Handle setting the banner link
    platform = request.data.get("platform", None)
    install_size = request.data.get("install_size", None)
    link = request.data.get("link", None)
    banner_link = request.data.get("banner_link", None)

    # Ensure platform is valid
    if platform not in ["Roblox", "Steam", "Party", "Other"]:
        return Response({"detail": "Invalid platform, games must be either Roblox, Steam, Party, or Other"},status=status.HTTP_400_BAD_REQUEST)
    
    if platform == "Steam" and not install_size:
        return Response({"detail": "Steam games must include an install_size"},status=status.HTTP_400_BAD_REQUEST)
    
    # If game is Party or Other, banner_link is required
    if platform in ["Party", "Other"] and not banner_link:
        return Response({"detail": f"{platform} games require a banner_link to be provided"},status=status.HTTP_400_BAD_REQUEST)

    # If game is Roblox or Steam, banner_link needs to be retrived
    if platform in ["Roblox", "Steam"]:
        # Get banner link
        banner_link = GameService.update_banner_link(platform, link)
        if not banner_link:
            return Response({"detail": "An error occured getting the banner link"}, status=status.HTTP_400_BAD_REQUEST)

    # Set banner link and serialize data
    request.data["banner_link"] = banner_link
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