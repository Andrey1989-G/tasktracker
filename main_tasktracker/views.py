from rest_framework import generics
from rest_framework.permissions import IsAuthenticated


from main_tasktracker.models import Task
from main_tasktracker.paginators import MainPaginator
from main_tasktracker.permissions import IsOwner
from main_tasktracker.serializers import TaskSerializer
from main_tasktracker.services import create_task, update_task


# Create your views here.

class TaskCreateAPIView(generics.CreateAPIView):
    """Представление для создания экземпляра модели поручения."""
    permission_classes = [IsAuthenticated]
    serializer_class = TaskSerializer


    def perform_create(self, serializer):
        """После создания (сохранения) экземпляра модели поручения
        вызываем функцию создания расписания напоминания."""
        new_task = serializer.save()
        create_task(new_task)

class TaskListAPIView(generics.ListAPIView):
    """Представление для отображения реквизитов списка поручений исполнителя."""
    permission_classes = [IsAuthenticated]
    serializer_class = TaskSerializer
    pagination_class = MainPaginator

    def get_queryset(self):
        """Накладываем отбор по исполнителям поручений."""
        return Task.objects.all()

class TaskViewAPIView(generics.RetrieveAPIView):
    """Отображение одного поручения"""
    permission_classes = [IsAuthenticated]
    serializer_class = TaskSerializer
    queryset = Task.objects.all()

class TaskUpdateAPIView(generics.UpdateAPIView):
    """Обновления данных поручения"""
    permission_classes = [IsAuthenticated]
    serializer_class = TaskSerializer
    queryset = Task.objects.all()

    def perform_update(self, serializer):
        """Обновление поручения"""
        new_task = serializer.save()
        update_task(new_task)

class TaskDeleteAPIView(generics.DestroyAPIView):
    """Удаление поручения"""
    permission_classes = [IsAuthenticated]
    serializer_class = TaskSerializer
    queryset = Task.objects.all()

class TaskExecutorListAPIView(generics.ListAPIView):
    """Отображение списка выполненных поручений исполнителем"""
    permission_classes = [IsAuthenticated]
    serializer_class = TaskSerializer

    def get_queryset(self):
        """Фильтр по признаку Подтверждение выполнения исполнителем"""
        return Task.objects.filter(readiness_executor=True)


class TaskBossListAPIView(generics.ListAPIView):
    """Отображение списка выполненных поручений начальником"""
    permission_classes = [IsAuthenticated]
    serializer_class = TaskSerializer

    def get_queryset(self):
        """Фильтр по признаку Подтверждение выполнения начальником"""
        return Task.objects.filter(readiness_boss=True)