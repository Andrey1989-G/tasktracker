from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from datetime import timedelta, datetime

from main_tasktracker.models import Task
from users.models import User
from django_celery_beat.models import PeriodicTask


class TaskTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email='test@test.ru', password='test', chat_id='1234567890')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        self.execute_id_01 = Task.objects.create(
            name='Поручение №1',
            description='Подпрыгни',
            priority=True,
            date_start=datetime.now(),
            date_end=datetime.now() + timedelta(days=3),
            readiness_boss=False,
            readiness_executor=False
        )

        self.execute_id_02 = Task.objects.create(
            name='Поручение №2',
            description='Поприседай',
            priority=True,
            date_start=datetime.now(),
            date_end=datetime.now() + timedelta(days=3),
            readiness_boss=False,
            readiness_executor=False
        )

        self.execute_id_03 = Task.objects.create(
            name='Поручение №3',
            description='Получи зарплату',
            priority=False,
            date_start=datetime.now(),
            date_end=datetime.now() + timedelta(days=3),
            readiness_boss=False,
            readiness_executor=False
        )

    # def test_create_periodic_task(self):
    #     """Тестирование создания задачи при создании поручения."""
    #
    #     data_execute = {'name': 'Поручение №4', 'description': 'Получи аванс', 'priority': 'True',
    #                   'date_start': 'False', 'date_end': 'True', 'readiness_boss': 1, 'readiness_executor': 60
    #                   }
    #
    #     self.client.post(
    #         '/create/',
    #         data=data_execute
    #     )
    #
    #     self.assertEquals(
    #         PeriodicTask.objects.filter(name=f'Task{self.execute_id_03.id + 1}').exists(),
    #         True
    #     )

    def test_create_execute_error_required_field(self):
        """Ошибка заполнения обязательного поля при создании поручения."""

        data_execute = {'description': 'Получи аванс', 'priority': 'True',
                        'date_start': 'False', 'date_end': 'True', 'readiness_boss': 'False',
                        'readiness_executor': 'False'
                        }

        response = self.client.post(
            '/create/',
            data=data_execute
        )

        self.assertEquals(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

        self.assertEquals(
            response.json(),
            {'name': ['Обязательное поле.']}
        )

    def test_create_execute(self):
        """Тестирование создания поручения."""

        data_execute = {'name': 'Поручение №4', 'description': 'Получи аванс', 'priority': 'True',
                        'readiness_boss': 'False', 'readiness_executor': 'False'}

        response = self.client.post(
            '/create/',
            data=data_execute
        )

        self.assertEquals(
            response.status_code,
            status.HTTP_201_CREATED
        )

        self.assertEquals(
            response.json(),
            {'id': self.execute_id_03.id + 1, 'name': 'Поручение №4', 'description': 'Получи аванс', 'priority': True,
             'readiness_boss': False, 'readiness_executor': False}
        )

    def test_create_periodic_task(self):
        """Тестирование создания задачи при создании поручения."""

        data_execute = {'name': 'Поручение №4', 'description': 'Получи аванс', 'priority': 'True',
                        'readiness_boss': 'False', 'readiness_executor': 'False'}

        self.client.post(
            '/create/',
            data=data_execute
        )

        self.assertEquals(
            PeriodicTask.objects.filter(name=f'Task{self.execute_id_03.id + 1}').exists(),
            True
        )

    def test_list_task(self):
        """Тестирование отображения поручений пользователя"""

        response = self.client.get(
            '/list/'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEquals(
            response.json().get('count') is not None and response.json().get('count') == 3,
            True
        )

    def test_view_task(self):
        """Тестирование отображения одного поручения."""

        response = self.client.get(
            f'/view/{self.execute_id_02.id}/'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.json(),
            {'id': self.execute_id_02.id, 'name': self.execute_id_02.name,
             'description': self.execute_id_02.description, 'priority': self.execute_id_02.priority,
             'date_start': self.execute_id_02.date_start, 'date_end': self.execute_id_02.date_end,
             'readiness_boss': self.execute_id_02.readiness_boss,
             'readiness_executor': self.execute_id_02.readiness_executor,
             }
        )

    def test_update_task(self):
        """Тестирование редактирования поручения. """

        data = {'id': self.execute_id_02.id, 'name': self.execute_id_02.name,
                'description': self.execute_id_02.description, 'priority': self.execute_id_02.priority,
                'date_start': self.execute_id_02.date_start, 'date_end': self.execute_id_02.date_end,
                'readiness_boss': self.execute_id_02.readiness_boss,
                'readiness_executor': self.execute_id_02.readiness_executor,
                }

        response = self.client.patch(
            f'/edit/{self.execute_id_02.id}/',
            data=data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.json(),
            {'id': self.execute_id_02.id, 'name': self.execute_id_02.name,
             'description': 'попытка поменять описание', 'priority': self.execute_id_02.priority,
             'date_start': self.execute_id_02.date_start, 'date_end': self.execute_id_02.date_end,
             'readiness_boss': self.execute_id_02.readiness_boss,
             'readiness_executor': self.execute_id_02.readiness_executor,
             }
        )

    def test_delete_task(self):
        """Тестирование удаления поручения."""

        response = self.client.delete(
            f'/delete/{self.execute_id_02.id}/',
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )
