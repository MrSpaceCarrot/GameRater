from django.core.management.base import BaseCommand, CommandError
from api.services import clear_expired_tokens
import logging

class Command(BaseCommand):
    help = 'Clear all expired auth tokens'

    def handle(self, *args, **kwargs):
        logger = logging.getLogger("services")
        logger.info("Clearing expired tokens...")
        kept, deleted = clear_expired_tokens()
        logger.info(f"Finished clearing expired tokens, Tokens kept: {kept}, Tokens deleted: {deleted}")
