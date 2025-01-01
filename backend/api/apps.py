from django.apps import AppConfig
import logging

logger = logging.getLogger(__name__)

class ApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api'

    def ready(self):
        try:
            from .scheduler import start_scheduler
            start_scheduler()
        except Exception as e:
            logger.error(f"Failed to start scheduler: {e}")