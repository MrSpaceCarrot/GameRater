from django.core.management.base import BaseCommand, CommandError
from api.services import GameService
import logging

class Command(BaseCommand):
    help = 'Update banner links for all games'

    def handle(self, *args, **kwargs):
        service = GameService()
        logger = logging.getLogger("services")
        logger.info("Starting to update banner links...")
        kept, updated, exceptions = service.update_banner_links()
        logger.info(f"Finished updating banner links, Links kept: {kept}, Links updated: {updated}, Links excepted: {exceptions}")
