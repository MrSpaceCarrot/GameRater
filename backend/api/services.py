import requests
from decouple import config
import re
import time
from .models import Game, DiscordUser, AuthToken, Rating
from datetime import datetime
from django.utils import timezone
from django.core.files.base import ContentFile
import logging
from typing import Tuple, Union
from PIL import Image
from io import BytesIO
from uuid import uuid4

# Handle logic for games
class GameService():
    def __init__(self):
        self.logger = logging.getLogger("services")

    # Get Roblox universe id for a link
    def get_roblox_universe_id(self, link):
        # Get place id using re
        place_id: str = (re.search(r'roblox\.com/games/(\d+)', link)).group(1)

        # Create session
        session = requests.Session()
        session.cookies[".ROBLOSECURITY"] = config("ROBLOX_COOKIE")

        # Get universe id
        universe_id_url = f"https://games.roblox.com/v1/games/multiget-place-details?placeIds={place_id}"
        universe_id_data = session.get(universe_id_url).json()
        if not universe_id_data or not "universeId" in universe_id_data[0]:
            return
        return [universe_id_data[0]["universeId"], session]
        
    # Get banner link for game
    def get_banner_link(self, platform, link):
        match platform:
            # Roblox Games
            case "Roblox":
                try:
                    universe_id, session = self.get_roblox_universe_id(link)

                    # Get banner url
                    banner_url = f"https://thumbnails.roblox.com/v1/games/multiget/thumbnails?universeIds={universe_id}&count=1&size=768x432&format=Png"
                    banner_url_data = session.get(banner_url).json()
                    if not "data" in banner_url_data or not len(banner_url_data["data"]) > 0 or not "thumbnails" in banner_url_data["data"][0]:
                        return

                    # Get link and close session
                    banner_link =  banner_url_data["data"][0]["thumbnails"][0]["imageUrl"]
                    session.close()
                except Exception:
                    return

            # Steam Games
            case "Steam":
                try:
                    app_id = re.search(r'/app/(\d+)', link).group(1)
                    banner_link = f"https://cdn.akamai.steamstatic.com/steam/apps/{app_id}/capsule_616x353.jpg"
                except Exception:
                    return
                
            # Other games
            case _:
                banner_link = None

        # Return link
        return banner_link
    
    # Get last updated
    def get_last_updated(self, platform, link):
        match platform:
            # Roblox Games
            case "Roblox":
                try:
                    universe_id, session = self.get_roblox_universe_id(link)

                    # Get last updated
                    last_updated_url = f"https://games.roblox.com/v1/games?universeIds={universe_id}"
                    last_updated_data = session.get(last_updated_url).json()
                    if not "data" in last_updated_data or not len(last_updated_data["data"]) > 0 or not "updated" in last_updated_data["data"][0]:
                        return
                    
                    # Get last updated and close session
                    last_updated = last_updated_data["data"][0]["updated"]
                    session.close()
                except Exception:
                    return
            
            case _:
                last_updated = None
            
        # Return date updated
        return last_updated
    
    # Get banner image binary from banner link
    def get_banner_image(self, game_id, banner_link):
        # Try open image from banner link
        try:
            response = requests.get(banner_link)
            img = Image.open(BytesIO(response.content))

            # Resize and crop image
            width, height = img.size
            scale_factor = max(int(config("BANNER_IMAGE_WIDTH")) / width, int(config("BANNER_IMAGE_HEIGHT")) / height)
            new_width = int(width * scale_factor)
            new_height = int(height * scale_factor)
            img = img.resize((new_width, new_height))

            left = (new_width - int(config("BANNER_IMAGE_WIDTH"))) // 2
            top = (new_height - int(config("BANNER_IMAGE_HEIGHT"))) // 2
            right = (new_width + int(config("BANNER_IMAGE_WIDTH"))) // 2
            bottom = (new_height + int(config("BANNER_IMAGE_HEIGHT"))) // 2
            img = img.crop((left, top, right, bottom))

            # Return contentfile
            buffer = BytesIO()
            img.save(buffer, format="PNG")
            buffer.seek(0)
            content_file = ContentFile(buffer.getvalue(), name=f"{game_id}.png")
            return content_file
        except Exception:
            return None
    
    # Update banner image for one game
    def update_banner_image(self, game_id):
        game = Game.objects.get(id=game_id)
        content_file = self.get_banner_image(game_id, game.banner_link)
        if content_file:
            self.logger.debug(f"Saving banner image for {game.name}")
            game.banner_image.delete()
            game.banner_image = None
            game.save()
            game.banner_image.save(f"{game_id}.png", content_file)
            game.save()
        else:
            self.logger.error(f"Error getting banner image for {game.name}")
    
    # Update average rating for a game
    def update_average_rating(self, game_id):
        # Get all ratings for the game, get average
        game_ratings = Rating.objects.filter(game_id=game_id)
        total_rating = 0
        number_ratings = 0
        for rating in game_ratings:
            if rating.rating not in [0, -1]:
                number_ratings += 1
                total_rating += rating.rating

        # Update game average rating
        game = Game.objects.get(id=game_id)
        try:
            new_average_rating = round((total_rating / number_ratings), 2)
            if new_average_rating != game.average_rating:
                self.logger.debug(f"Updating average rating for {game.name} from {game.average_rating} to {new_average_rating}")
                game.average_rating = new_average_rating
            else:
                self.logger.debug(f"Keeping average rating for {game.name} at {game.average_rating}")
        except ZeroDivisionError as e:
            game.average_rating = None
            self.logger.debug(f"Updating average rating for {game.name} to None")
        game.save()

    # Update popularity score for a game
    def update_popularity_score(self, game_id):
        game = Game.objects.get(id=game_id)
        if not game.average_rating:
            return

        people_rated = Rating.objects.filter(game_id=game_id, rating__gt=0).count()
        people_total = int(config("PEOPLE_CONSTANT"))
        new_popularity_score = round(min(1, (game.average_rating) * 0.12 * (people_rated / people_total)), 4)

        if new_popularity_score != game.popularity_score:
            self.logger.debug(f"Updating popularity score for {game.name} from {game.popularity_score} to {new_popularity_score}")
            game.popularity_score = new_popularity_score
        else:
            self.logger.debug(f"Keeping popularity score for {game.name} at {game.popularity_score}")
        game.save()

    # Update banner links for all games
    def update_banner_links(self) -> Tuple[int, int, int]:
        kept = 0
        updated = 0
        exceptions = 0

        games = Game.objects.all().order_by('name')
        for game in games:
            if game.update_banner_link == False:
                self.logger.debug(f"Keeping banner link for {game.name} due to exception")
                exceptions += 1
                continue
            else:
                new_banner_link = self.get_banner_link(game.platform, game.link)
                
                time.sleep(1)
                if new_banner_link:
                    if new_banner_link == game.banner_link:
                        self.logger.debug(f"Keeping banner link for {game.name}")
                        kept += 1
                    else:
                        self.logger.debug(f"Changing banner link for {game.name} from {game.banner_link} to {new_banner_link}")
                        game.banner_link = new_banner_link
                        game.save()
                        self.update_banner_image(game.id)
                        updated += 1
                else:
                    self.logger.debug(f"Keeping banner link for {game.name}")
                    kept += 1

        return kept, updated, exceptions

    # Update last updated for all games
    def update_last_updated(self) -> Tuple[int, int]:
        kept = 0
        updated = 0

        games = Game.objects.all().order_by('name')
        for game in games:
            new_last_updated = self.get_last_updated(game.platform, game.link)
            
            time.sleep(1)
            if new_last_updated:
                parsed_new_last_updated = datetime.fromisoformat(new_last_updated).replace(microsecond=0)
                parsed_old_last_updated = game.last_updated.replace(microsecond=0)

                if parsed_new_last_updated == parsed_old_last_updated:
                    self.logger.debug(f"Keeping last updated for {game.name}")
                    kept += 1
                else:
                    self.logger.debug(f"Changing last updated for {game.name} from {parsed_old_last_updated} to {parsed_new_last_updated}")
                    game.last_updated = parsed_new_last_updated
                    game.save()
                    updated += 1
            else:
                self.logger.debug(f"Keeping last updated for {game.name}")
                kept += 1

        return kept, updated
    
    # Update banner images for all games
    def update_banner_images(self):
        games = Game.objects.all()
        for game in games:
            self.update_banner_image(game.id)
            time.sleep(1)

    # Update average ratings for all games
    def update_average_ratings(self):
        games = Game.objects.all()
        for game in games:
            self.update_average_rating(game.id)

    # Update popularity score for all games
    def update_popularity_scores(self):
        games = Game.objects.all()
        for game in games:
            self.update_popularity_score(game.id)

    # Sort tags alphabetically for all games
    def sort_tags(self) -> Tuple[int, int]:
        kept = 0
        changed = 0
        games = Game.objects.all().order_by('name')

        for game in games:
            tags = game.tags
            sorted_tags = sorted(tags)
            if tags != sorted_tags:
                self.logger.debug(f"Changed order of tags for {game.name}")
                game.tags = sorted_tags
                game.save()
                changed += 1
            else:
                self.logger.debug(f"Tag order retained for {game.name}")
                kept += 1

        return kept, changed

# Get user from token used
def get_user_from_auth_header(request: requests.Request) -> Union[DiscordUser, None]:
    try:
        auth_header = request.headers['Authorization']
        token = auth_header.split(' ')[1]
        token_object = AuthToken.objects.get(token=token)
        user_object = DiscordUser.objects.get(id=token_object.user_id)
        return user_object
    except AuthToken.DoesNotExist:
        return None

# Clear expired tokens
def clear_expired_tokens() -> Tuple[int, int]:
    logger = logging.getLogger("services")
    kept = 0
    deleted = 0
    token_objects = AuthToken.objects.all()

    for token_object in token_objects:
        if timezone.now() > token_object.expiry_date:
            logger.debug(f"Deleting expired token {token_object.id}")
            token_object.delete()
            deleted += 1
        else:
            logger.debug(f"Keeping token {token_object.id}")
            kept += 1

    return kept, deleted