from django.core.management.base import BaseCommand, CommandError
from api.services import GameService
import logging

class Command(BaseCommand):
    help = 'Sort tags alphabetically for all games'

    def handle(self, *args, **kwargs):
        service = GameService()
        logger = logging.getLogger("services")
        logger.info("Sorting tags...")
        kept, changed = service.sort_tags()
        logger.info(f"Finished sorting tags, Orders kept: {kept}, Orders changed: {changed}")
