from django.core.management import call_command
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """
        Django custom management command for DB Migration

        syntax: python manage.py setup
    """
    def handle(self, *args, **options) -> None:
        call_command('makemigrations')
        call_command('migrate')
