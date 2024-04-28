from rest_framework import serializers
from .models import ExecutorTask, StatusTask, Task


class TaskSerializer(serializers.ModelSerializer):
    """Сериализатор для модели поручений"""
    class Meta:
        model = Task
        fields = ['name_task', 'description', 'date_start', 'date_end', 'period', 'id_boss', 'id_executor', 'priority', 'readiness_boss']


class UserTaskSerializer(serializers.ModelSerializer):
    """Сериализатор для модели поручений исполнителя"""
    class Meta:
        model = ExecutorTask
        fields = '__all__'


class StatusTaskSerializer(serializers.ModelSerializer):
    """Сериализатор для модели проверки статуса выполнения"""
    class Meta:
        model = StatusTask
        fields = '__all__'
