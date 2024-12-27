from django.core.management.base import BaseCommand, CommandError
from api.services import GameService

class Command(BaseCommand):
    help = 'Update average ratings for all games'

    def handle(self, *args, **kwargs):
        service = GameService()
        self.stdout.write("Starting to update average ratings")
        service.update_average_ratings()
        self.stdout.write("Finished updating average ratings")
