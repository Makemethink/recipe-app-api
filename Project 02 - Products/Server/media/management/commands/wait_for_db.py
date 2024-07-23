from django.core.management.base import BaseCommand
import time
import sys
from django.db import connections, OperationalError
from django.conf import settings
# from django.db import connection


class Command(BaseCommand):
    """
        Django custom management command for Wait for DB

        use case: In Docker the wait for DB was mandatory to check DB Connection in another container before begin

        usage: If the DB don't have required schema it will create it by changing django settings
        syntax: python manage.py setup
    """
    def handle(self, *args, **options) -> None:

        self.stdout.write('Waiting for the DB ...')

        # Modify settings dynamically
        settings.DATABASES['default']['NAME'] = ''

        import django
        django.setup()     # The changed django settings scope is up to this custom management python file

        count: int = 0
        max_retry_count: int = 5
        is_db_up: bool = False

        while is_db_up is False:
            try:
                if count > max_retry_count:
                    break

                # Alternate connection.ensure_connection()
                default_connection = connections['default']
                with default_connection.cursor() as cursor:
                    cursor.execute("CREATE DATABASE IF NOT EXISTS media;")

                is_db_up = True
                self.stdout.write(self.style.SUCCESS('Success'))

            except OperationalError:
                self.stdout.write(self.style.ERROR('Database unavailable, waiting 3 seconds'))
                time.sleep(3)
                count += 1

        self.stdout.write(self.style.SUCCESS('Out from wait for DB'))
        if is_db_up is False:
            sys.exit(1)
