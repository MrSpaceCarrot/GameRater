from rest_framework import serializers
from .models import Game, Tag, Rating, AuthToken, DiscordUser, Tag
from .services import GameService, get_user_from_auth_header
from rest_framework.authentication import get_authorization_header

class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = '__all__'
        read_only_fields = ['added_by']

    name = serializers.CharField(required=True, max_length=100)
    platform = serializers.CharField(required=True, max_length=10)
    link = serializers.CharField(required=True, max_length=300)
    banner_link = serializers.CharField(required=False, max_length=300, allow_blank=True)
    min_party_size = serializers.IntegerField(required=True)
    max_party_size = serializers.IntegerField(required=True)
    tags = serializers.JSONField(required=True)

    def validate_platform(self, platform):
        if platform not in ["Roblox", "Steam", "Party", "Other"]:
            raise serializers.ValidationError("Must be either 'Roblox', 'Steam', 'Party', or 'Other'")
        return platform
    
    def validate_min_party_size(self, min_party_size):
        if min_party_size < 1 or min_party_size > 16:
            raise serializers.ValidationError("Must be between 1 and 16")
        return min_party_size
    
    def validate_max_party_size(self, max_party_size):
        if max_party_size < 1 or max_party_size > 16:
            raise serializers.ValidationError("Must be between 1 and 16")
        return max_party_size
    
    def validate_tags(self, tags):
        if type(tags) != list:
            raise serializers.ValidationError("Must be a list of strings")
        if len(tags) < 2:
            raise serializers.ValidationError("Must provide at least 2")
        if len(tags) > 5:
            raise serializers.ValidationError("Must provide fewer than 6")
        
        db_tags = list(Tag.objects.values_list('tag', flat=True))
        for tag in tags:
            if tag not in db_tags:
                raise serializers.ValidationError(f"'{tag}' tag is not in the whitelist")         
        return sorted(tags)
            
    def validate(self, data):
        # Variables
        name = data.get("name")
        platform = data.get("platform")
        link = data.get("link")
        banner_link = data.get("banner_link")

        # Ensure game is unique
        if Game.objects.filter(name=name).exists():
            raise serializers.ValidationError({"duplicate": "This game has already been added"})
        if Game.objects.filter(link=link).exists() and platform != "Party":
            raise serializers.ValidationError({"duplicate": "This game has already been added"})

        # Ensure banner link is set
        game_service = GameService()
        if platform in ["Party", "Other"] and not banner_link:
            raise serializers.ValidationError({"banner_link": f"Must be specified when platform is '{platform}'"})
        elif platform in ["Roblox", "Steam"]:
            data["banner_link"] = game_service.get_banner_link(platform, link)
            if not data["banner_link"]:
                raise serializers.ValidationError({"banner_link": f"Failed to retrieve from {platform} API. Link is invalid"})
            
        # Ensure last updated is set
        if platform == "Roblox":
            data["last_updated"] = game_service.get_last_updated(platform, link)
            if not data["last_updated"]:
                raise serializers.ValidationError({"last_updated": f"Failed to retrieve from {platform} API. Link is invalid"})
            
        # Ensure added by is set
        request_user = get_user_from_auth_header(self.context)
        data["added_by"] = request_user

        # Check user has permissions
        if self.instance:
            if request_user.id != self.instance.added_by.id:
                raise serializers.ValidationError({"Permissions": f"You do not have permission to modify this resource"})
             
        return data
    

class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = '__all__'

    game = serializers.PrimaryKeyRelatedField(queryset=Game.objects.all())
    rating = serializers.IntegerField(required=True)
    
    def validate_rating(self, rating):
        if rating < -1 or rating > 10:
            raise serializers.ValidationError({"Rating": f"Rating must be between 1 and 10, 0 for unrated, -1 for ignored"})
        return rating
    
    def create(self, validated_data):
        request_user = get_user_from_auth_header(self.context)
        request_game = validated_data["game"]
        request_rating = validated_data["rating"]

        rating, created = Rating.objects.update_or_create(
            user=request_user,
            game=request_game,
            defaults={'rating': request_rating}
        )
        return rating


class DiscordUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiscordUser
        fields = '__all__'
        

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'

    tag = serializers.CharField(required=True)
