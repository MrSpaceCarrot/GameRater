import requests
from decouple import config
import re

# Handle logic for games
class GameService():
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
        
    # Set banner art for game
    def get_banner_link(self, platform, link):
        match platform:
            # Roblox Games
            case "Roblox":
                universe_id, session = self.get_roblox_universe_id(link)

                # Get banner url
                banner_url = f"https://thumbnails.roblox.com/v1/games/multiget/thumbnails?universeIds={universe_id}&count=1&size=768x432&format=Png"
                banner_url_data = session.get(banner_url).json()
                if not "data" in banner_url_data or not len(banner_url_data["data"]) > 0 or not "thumbnails" in banner_url_data["data"][0]:
                    return

                # Get link and close session
                banner_link =  banner_url_data["data"][0]["thumbnails"][0]["imageUrl"]
                session.close()

            # Steam Games
            case "Steam":
                app_id = re.search(r'/app/(\d+)', link).group(1)
                banner_link = f"https://cdn.akamai.steamstatic.com/steam/apps/{app_id}/capsule_616x353.jpg"

        # Return link
        return banner_link
    
    # Set last updated
    def get_last_updated(self, platform, link):
        match platform:
            # Roblox Games
            case "Roblox":  
                universe_id, session = self.get_roblox_universe_id(link)

                # Get last updated
                last_updated_url = f"https://games.roblox.com/v1/games?universeIds={universe_id}"
                last_updated_data = session.get(last_updated_url).json()
                if not "data" in last_updated_data or not len(last_updated_data["data"]) > 0 or not "updated" in last_updated_data["data"][0]:
                    return
                
                # Get last updated and close session
                last_updated = last_updated_data["data"][0]["updated"]
                session.close()
            
            case "Steam":
                pass
            
        # Return date updated
        return last_updated
