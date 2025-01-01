from django.core.management.base import BaseCommand, CommandError
from api.services import GameService
import logging

class Command(BaseCommand):
    help = 'Update last updated for all games'

    def handle(self, *args, **kwargs):
        service = GameService()
        logger = logging.getLogger("services")
        logger.info("Starting to update last updated")
        kept, updated = service.update_last_updated()
        logger.info(f"Finished updating last updated, Dates kept: {kept}, Dates updated: {updated}")
