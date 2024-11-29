import requests
from decouple import config
import re

# Handle logic for games
class GameService():
    # Set banner art for game
    def update_banner_link(platform, link):
        match platform:
            # Roblox Games
            case "Roblox":
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
                universe_id = universe_id_data[0]["universeId"]

                # Get banner url
                banner_url = f"https://thumbnails.roblox.com/v1/games/multiget/thumbnails?universeIds={universe_id}&count=1&size=768x432&format=Png"
                banner_url_data = session.get(banner_url).json()
                if not "data" in banner_url_data or not len(banner_url_data["data"]) > 0 or not "thumbnails" in banner_url_data["data"][0]:
                    return

                # Set link and close session
                banner_link =  banner_url_data["data"][0]["thumbnails"][0]["imageUrl"]
                session.close()

            # Steam Games
            case "Steam":
                app_id = re.search(r'/app/(\d+)', link).group(1)
                banner_link = f"https://cdn.akamai.steamstatic.com/steam/apps/{app_id}/capsule_616x353.jpg"

        # Return link
        return banner_link
