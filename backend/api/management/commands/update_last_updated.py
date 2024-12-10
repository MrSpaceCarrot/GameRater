from django.core.management.base import BaseCommand, CommandError
from api.services import GameService

class Command(BaseCommand):
    help = 'Update last updated for all games'

    def handle(self, *args, **kwargs):
        service = GameService()
        self.stdout.write("Starting to update last updated")
        service.update_last_updated()
        self.stdout.write("Finished updating last updated")
