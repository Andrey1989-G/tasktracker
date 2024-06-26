from datetime import datetime

from django.core.exceptions import ValidationError
from django.db import models
from django.core.validators import RegexValidator, MaxLengthValidator, MinValueValidator, MaxValueValidator
from django.utils import timezone

from users.models import User


# Create your models here.
class Task(models.Model):
    """Модель поручений"""

    PERIOD_DAY01 = 1
    PERIOD_DAY02 = 2
    PERIOD_DAY03 = 3
    PERIOD_DAY04 = 4
    PERIOD_DAY05 = 5
    PERIOD_DAY06 = 6
    PERIOD_DAY07 = 7

    PERIODS = (
        (PERIOD_DAY01, 'раз в день'),
        (PERIOD_DAY02, 'раз в 2 дня'),
        (PERIOD_DAY03, 'раз в 3 дня'),
        (PERIOD_DAY04, 'раз в 4 дня'),
        (PERIOD_DAY05, 'раз в 5 дней'),
        (PERIOD_DAY06, 'раз в 6 дней'),
        (PERIOD_DAY07, 'раз в неделю'),
    )

    name_task = models.CharField(max_length=50, blank=True, verbose_name='Название задачи')
    description = models.CharField(blank=True, null=True, validators=[
        MaxLengthValidator(255, message='Длина поля не должна превышать 255 символов.')
    ],
                                   verbose_name='Описание задачи')
    priority = models.BooleanField(default=False, verbose_name='высокий приоритет')
    date_start = models.DateTimeField(default=datetime.now, verbose_name='Начало выполнения поручения')
    date_end = models.DateField(blank=True, null=True, validators=[
        RegexValidator(
            regex=r'^\d{4}-\d{2}-\d{2}$',
            message='Недопустимый формат. Введите дату в формате dd-mm-yyy',
            code='invalid_date',
        )
    ],
                                verbose_name='Окончание выполнения поручения')
    id_executor = models.ForeignKey(User, on_delete=models.CASCADE, null=True, verbose_name='Имя_исполнителя', related_name="tasks_as_executor")
    id_boss = models.ForeignKey(User, on_delete=models.CASCADE, null=True, verbose_name='Имя_руководителя', related_name="tasks_as_boss")
    readiness_boss = models.BooleanField(default=False, verbose_name='Подтверждение выполнения начальником')
    readiness_executor = models.BooleanField(default=False, verbose_name='Подтверждение выполнения исполнителем')
    period = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(7)], default=PERIOD_DAY01,
                                 choices=PERIODS, verbose_name='периодичность')


    def validate_date(self):
        if self < timezone.now().date():
            raise ValidationError('Нельзя поручить задачу задним числом.')

    def clean(self):
        if self.date_start and self.date_end and self.date_end < self.date_start:
            raise ValidationError("Дата начала выполнения поручения должна быть позже дедлайна.")

    def __str__(self):
        return f"{self.name} {self.description}"


class ExecutorTask(models.Model):
    """Модель поручений исполнителя"""
    worker_id = models.ForeignKey(User, on_delete=models.CASCADE)
    task_id = models.ForeignKey(Task, on_delete=models.CASCADE)
    family = models.ForeignKey(User, on_delete=models.CASCADE, related_name="family_as_executor")

    def __str__(self):
        return f"Executor: {self.worker_id.name} {self.worker_id.family}, Task: {self.task_id.name}"


class BossTask(models.Model):
    """Модель поручений руководителя"""
    worker_id = models.ForeignKey(User, on_delete=models.CASCADE)
    task_id = models.ForeignKey(Task, on_delete=models.CASCADE)
    family = models.ForeignKey(User, on_delete=models.CASCADE, related_name="family_as_boss")

    def __str__(self):
        return f"Boss: {self.worker_id.name} {self.worker_id.family}, Task: {self.task_id.name}"


class StatusTask(models.Model):
    """Модель проверки статуса выполнения"""
    readiness_boss = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="tasks_as_boss")
    task_id = models.ForeignKey(Task, on_delete=models.CASCADE)
    readiness_executor = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="tasks_as_executor")

    def __str__(self):
        return f"Task ID: {self.task_id.name} Execution:{self.readiness_executor} Status: {self.readiness_boss}"
