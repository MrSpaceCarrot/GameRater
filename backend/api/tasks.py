from celery import shared_task
from django.core.management import call_command
from celery.schedules import crontab
from django_celery_beat.models import PeriodicTask, IntervalSchedule, CrontabSchedule
import json
from django.utils import timezone
from datetime import timedelta

def add_one_min():
    return timezone.now() + timedelta(minutes=10)

@shared_task
def run_management_command(command_name, *args, **kwargs):
    try:
        call_command(command_name, *args, **kwargs)
        return f"Command '{command_name}' executed successfully."
    except Exception as e:
        return f"Error executing command '{command_name}': {str(e)}"

def schedule_celery_task(name, minute):
    schedule, created = CrontabSchedule.objects.get_or_create(minute=minute)

    PeriodicTask.objects.update_or_create(
        name=f"{name}_job",
        defaults={
            'task': 'api.tasks.run_management_command',
            'crontab': schedule,
            'args': json.dumps([f"{name}"]),
            'enabled': True,
        },
    )
