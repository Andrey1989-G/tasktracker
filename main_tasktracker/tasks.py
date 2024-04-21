from celery import shared_task
from requests import post
from django.conf import settings

from main_tasktracker.models import Task


@shared_task
def send_message_bot(task_id):
    """Отправка сообщений в телеграм"""
    reminder = Task.objects.get(id=task_id)
    post(
        url=f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage",
        data={
            'chat_id': reminder.owner.phone,
            'text': f'Срок выполнения поручения истек. Прошу выполнить поручение'
                    f' [{reminder.name} в кратчайшие сроки] !'
        }
    )
