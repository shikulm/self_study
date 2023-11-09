# Заполнение справочников товаров и категорий

from django.core.management import BaseCommand, call_command
from django.core import management

# from users.models import User


class Command(BaseCommand):
    help = 'Load data into database'

    def handle(self, *args, **options):

        management.call_command('loaddata', 'data2.json', '--natural-foreign')

        # Удаляем всех пользователей
        # User.objects.all().delete()
        #
        #
        # # Восстанавливаем данные из json файла
        # # python manage.py loaddata data.json
        # call_command('loaddata', 'data2.json')
        # # loaddata data.json