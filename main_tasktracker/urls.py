from django.urls import path
from main_tasktracker.apps import MainTasktrackerConfig
from main_tasktracker.views import TaskCreateAPIView, TaskListAPIView, TaskViewAPIView, TaskUpdateAPIView, \
    TaskExecutorListAPIView, TaskBossListAPIView, TaskDeleteAPIView

from django.urls import re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

...

schema_view = get_schema_view(
   openapi.Info(
      title="Tasktracker API",
      default_version='v1',
      description="Описание",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

app_name = MainTasktrackerConfig.name

urlpatterns = [
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('create/', TaskCreateAPIView.as_view(), name='task_create'),
    path('list/', TaskListAPIView.as_view(), name='task_list'),
    path('view/<int:pk>/', TaskViewAPIView.as_view(), name='task_view'),
    path('edit/<int:pk>/', TaskUpdateAPIView.as_view(), name='task_edit'),
    path('delete/<int:pk>/', TaskDeleteAPIView.as_view(), name='task_delete'),
    path('list_executor/', TaskExecutorListAPIView.as_view(), name='task_list_executor'),
    path('list_boss/', TaskBossListAPIView.as_view(), name='task_list_boss'),

]