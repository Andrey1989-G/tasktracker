from django.urls import path
from main_tasktracker.apps import MainTasktrackerConfig
from main_tasktracker.views import TaskCreateAPIView, TaskListAPIView, TaskViewAPIView, TaskUpdateAPIView, \
    UsefulHabitDeleteAPIView, TaskExecutorListAPIView, TaskBossListAPIView

app_name = MainTasktrackerConfig.name

urlpatterns = [
    path('create/', TaskCreateAPIView.as_view(), name='task_create'),
    path('list/', TaskListAPIView.as_view(), name='task_list'),
    path('view/<int:pk>/', TaskViewAPIView.as_view(), name='tasktask_view'),
    path('edit/<int:pk>/', TaskUpdateAPIView.as_view(), name='task_edit'),
    path('delete/<int:pk>/', UsefulHabitDeleteAPIView.as_view(), name='task_delete'),
    path('list_executor/', TaskExecutorListAPIView.as_view(), name='task_list_executor'),
    path('list_boss/', TaskBossListAPIView.as_view(), name='task_list_boss'),
]