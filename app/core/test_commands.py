from django.test import TestCase
from django.db import connection


class DatabaseConnectionTestCase(TestCase):
    def test_database_connection(self):
        try:
            connection.ensure_connection()
        except Exception as e:
            self.fail(f"Database connection failed: {e}")
