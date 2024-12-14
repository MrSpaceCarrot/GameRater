from django.core.management.base import BaseCommand, CommandError
from api.services import GameService

class Command(BaseCommand):
    help = 'Sort tags alphabetically for all games'

    def handle(self, *args, **kwargs):
        service = GameService()
        self.stdout.write("Sorting tags")
        service.sort_tags()
        self.stdout.write("Finished sorting tags")
