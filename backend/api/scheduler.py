import os
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.executors.pool import ThreadPoolExecutor
from apscheduler.jobstores.memory import MemoryJobStore
from django.core.management import call_command
import logging

logger = logging.getLogger(__name__)

scheduler = None

def start_scheduler():
    global scheduler

    if os.environ.get('SCHEDULER_RUNNING') == 'true':
        logger.info("Scheduler already running. Skipping initialization.")
        return

    os.environ['SCHEDULER_RUNNING'] = 'true'

    if scheduler is None or not scheduler.running:
        jobstores = {'default': MemoryJobStore()}
        executors = {'default': ThreadPoolExecutor(10)}
        job_defaults = {'coalesce': True, 'max_instances': 10}

        scheduler = BackgroundScheduler(jobstores=jobstores, executors=executors, job_defaults=job_defaults)

        scheduler.add_job(call_command, 'cron', args=['clear_expired_tokens'], minute=20, id='clear_expired_tokens_job')
        scheduler.add_job(call_command, 'cron', args=['sort_tags'], minute=40, id='sort_tags_job')
        scheduler.add_job(call_command, 'cron', args=['update_average_ratings'], minute=0, id='update_average_ratings_job')
        scheduler.add_job(call_command, 'cron', args=['update_banner_images'], minute='0,30', id='update_banner_images_job')
        scheduler.add_job(call_command, 'cron', args=['update_popularity_scores'], minute=5, id='update_popularity_scores_job')
        scheduler.add_job(call_command, 'cron', args=['update_last_updated'], minute='15,45', id='update_last_updated_job')

        scheduler.start()
        logger.info("Scheduler started.")
    else:
        logger.info("Scheduler is already running.")