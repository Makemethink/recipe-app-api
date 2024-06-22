"""
Django command to wait for the database to be available.
"""
import time
import os
import MySQLdb as mysql
from django.core.management.base import BaseCommand
from django.db.utils import OperationalError


class Command(BaseCommand):
    """
        Django command to wait for DB
    """

    def handle(self, *args, **options):
        self.stdout.write('Waiting for the DB ...')

        count = 0
        max_count = 10

        db_up: bool = False
        while db_up is False:
            try:
                if count > max_count:
                    break

                conn = mysql.connect(  # Replace with your database name
                    user=os.environ.get('DB_USER'),  # Replace with your MySQL username
                    password=os.environ.get('DB_PASS'),  # Replace with your MySQL password
                    host=os.environ.get('DB_HOST'),  # Replace with your MySQL host address
                    port=3306)

                cursor = conn.cursor()
                cursor.execute(f"CREATE DATABASE {os.environ.get('DB_NAME')}")
                conn.close()
                print('Successfully connected to the database')
                db_up = True
            except mysql.Error as e:
                print(f'Error connecting to the database: {e}')
                count = count+1
                time.sleep(5)

        self.stdout.write(self.style.SUCCESS('Database available'))


