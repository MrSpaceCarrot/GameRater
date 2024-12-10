from django.core.management.base import BaseCommand, CommandError
from api.services import GameService

class Command(BaseCommand):
    help = 'Update banner images for all games'

    def handle(self, *args, **kwargs):
        service = GameService()
        self.stdout.write("Starting to update banner images")
        service.update_banner_images()
        self.stdout.write("Finished updating banner images")
