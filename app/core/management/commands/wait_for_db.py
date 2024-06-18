"""
Django command to wait for the database to be available.
"""
import time

from django.core.management.base import BaseCommand
from django.db.utils import OperationalError
from mysql.connector.errors import OperationalError as mysql_OPError


class Command(BaseCommand):
    """
        Django command to wait for DB
    """

    def handle(self, *args, **options):
        self.stdout.write('Waiting for the DB ...')
        db_up: bool = False
        while db_up is False:
            try:
                self.check(databases=['default'])
                db_up = True
            except (mysql_OPError, OperationalError) as e:
                self.stdout.write('DB unavailable, waiting for some time')
                self.stdout.write(e)
                time.sleep(3)

        self.stdout.write(self.style.SUCCESS('Database available'))


