from django_celery_beat.models import CrontabSchedule, PeriodicTask
from config import settings


# функции для работы с поручениями
def create_task(task):
    """Создание поручения"""
    schedule, created = CrontabSchedule.objects.get_or_create(
        minute=task.date_start.minute,
        hour=task.date_start.hour,
        day_of_week=f'*/{task.period}',
        month_of_year='*',
        timezone=settings.TIME_ZONE
    )

    PeriodicTask.objects.create(
        crontab=schedule,
        name=f'Task{task.id}',
        task='main_tasktracker.tasks.send_message_bot',
        args=[task.id],
    )


def delete_task(task):
    """Удаление поручения"""

    PeriodicTask.objects.filter(name=f'Task{task.id}').delete()


def update_task(task):
    """Пересоздание поручения"""
    delete_task(task)
    create_task(task)
