from backend.api.services import GameService
service = GameService()
print(service.get_last_updated("Roblox", "https://www.roblox.com/games/381674682/Wheres-the-Baby"))