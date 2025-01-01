from django.core.management.base import BaseCommand, CommandError
from api.services import GameService
import logging

class Command(BaseCommand):
    help = 'Update banner images for all games'

    def handle(self, *args, **kwargs):
        service = GameService()
        logger = logging.getLogger("services")
        logger.info("Starting to update banner images")
        kept, updated, exceptions = service.update_banner_images()
        logger.info(f"Finished updating banner images, Images kept: {kept}, Images updated: {updated}, Images excepted: {exceptions}")
