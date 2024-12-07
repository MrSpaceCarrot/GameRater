from rest_framework import serializers
from .models import Game, Tag, AuthToken, DiscordUser, Tag
from .services import GameService
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
        if min_party_size < 2 or min_party_size > 16:
            raise serializers.ValidationError("Must be between 2 and 16")
        return min_party_size
    
    def validate_max_party_size(self, max_party_size):
        if max_party_size < 2 or max_party_size > 16:
            raise serializers.ValidationError("Must be between 2 and 16")
        return max_party_size
    
    def validate_tags(self, tags):
        if type(tags) != list:
            raise serializers.ValidationError("Must be a list of strings")
        if len(tags) < 2:
            raise serializers.ValidationError("Must provide at least 2")
        if len(tags) > 5:
            raise serializers.ValidationError("Must provide fewer than 5")
        
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
        if Game.objects.filter(name=name).exists() or Game.objects.filter(link=link).exists():
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
        try:
            header = self.context
            token = header.split(' ')[1]
            token_object = AuthToken.objects.get(token=token)
            user_object = DiscordUser.objects.get(id=token_object.user_id)
            data["added_by"] = user_object
        except Exception:
            data["added_by"] = None
             
        return data
        

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'

    tag = serializers.CharField(required=True)
