from django.core.management.base import BaseCommand, CommandError
from api.services import GameService
import logging

class Command(BaseCommand):
    help = 'Update banner images for all games'

    def handle(self, *args, **options):
        service = GameService()
        logger = logging.getLogger("services")

        if options['game_id']:
            service.update_banner_image(options['game_id'])
        else:
            logger.info("Starting to update banner images...")
            service.update_banner_images()
            logger.info(f"Finished updating banner images")

    def add_arguments(self, parser):
        parser.add_argument(
            "--game_id",
            help="Specify a specific game id to update the banner image of",
        )