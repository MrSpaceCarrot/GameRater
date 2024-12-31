from django.core.management.base import BaseCommand, CommandError
from api.services import GameService, clear_expired_tokens

class Command(BaseCommand):
    help = 'Clear all expired auth tokens'

    def handle(self, *args, **kwargs):
        self.stdout.write("Clearing expired tokens")
        clear_expired_tokens()
        self.stdout.write("Finished clearing expired tokens")
