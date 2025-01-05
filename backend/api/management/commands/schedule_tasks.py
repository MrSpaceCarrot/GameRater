from django.core.management.base import BaseCommand, CommandError
import logging
from api.tasks import schedule_celery_task

class Command(BaseCommand):
    help = 'Schedule all maintanence tasks'

    def handle(self, *args, **kwargs):
        logger = logging.getLogger("services")
        logger.info("Scheduling tasks")

        schedule_celery_task("update_banner_images", "0,30")
        schedule_celery_task("update_last_updated", "15,45")
        schedule_celery_task("update_average_ratings", "5")
        schedule_celery_task("update_popularity_scores", "10")
        schedule_celery_task("clear_expired_tokens", "35")
        schedule_celery_task("sort_tags", "40")

        logger.info(f"Finished scheduling tasks")
