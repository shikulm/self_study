# Заполнение справочников товаров и категорий

from django.core.management import BaseCommand, call_command
from django.core import management



class Command(BaseCommand):

    help = 'Load data into database'

    def handle(self, *args, **options):
        management.call_command('dumpdata', '--exclude', 'auth.permission', '--exclude', 'contenttypes', output='data2.json')

        # call_command('dumpdata', ' -o data2.json')
        #
        # python -Xutf8 manage.py dumpdata -o data2.json
        # loaddata data.json

        # ./manage.py dumpdata --exclude auth.permission --exclude contenttypes > db.json

        # ./manage.py loaddata data2.json