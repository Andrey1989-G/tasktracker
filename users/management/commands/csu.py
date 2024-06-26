from django.core.management import BaseCommand
from users.models import User

from os import getenv


class Command(BaseCommand):

    def handle(self, *args, **options):
        user = User.objects.create(
            email=getenv('ADMIN_EMAIL'),
            phone=1234,
            name='Admin',
            family='adminsky',
            is_staff=True,
            is_superuser=True,
            is_active=True
        )

        user.set_password(getenv('ADMIN_PASSWORD'))
        user.save()
