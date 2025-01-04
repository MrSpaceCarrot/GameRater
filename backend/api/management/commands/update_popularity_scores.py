from django.core.management.base import BaseCommand, CommandError
from api.services import GameService
import logging

class Command(BaseCommand):
    help = 'Update popularity scores for all games'

    def handle(self, *args, **kwargs):
        service = GameService()
        logger = logging.getLogger("services")
        logger.info("Starting to update popularity scores...")
        service.update_popularity_scores()
        logger.info("Finished updating popularity scores")
