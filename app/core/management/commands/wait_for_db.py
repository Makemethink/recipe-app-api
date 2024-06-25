"""
Django command to wait for the database to be available.
"""
import time
import os
import MySQLdb as Mysql
from django.core.management.base import BaseCommand


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

                # Fetch environment variables
                db_user = os.environ.get('DB_USER')
                db_pass = os.environ.get('DB_PASS')
                db_host = os.environ.get('DB_HOST')
                db_name = os.environ.get('DB_NAME')

                # Establish MySQL connection
                conn = Mysql.connect(
                    user=db_user,
                    password=db_pass,
                    host=db_host,
                    port=3306
                )

                cursor = conn.cursor()
                cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
                conn.close()
                print('Successfully connected to the database')
                db_up = True
            except Mysql.Error as e:
                print(f'Error connecting to the database: {e}')
                count = count+1
                time.sleep(5)

        self.stdout.write(self.style.SUCCESS('Database available'))
