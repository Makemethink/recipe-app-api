from unittest.mock import patch

from django.core.management import call_command
from django.test import SimpleTestCase


@patch('core.management.commands.wait_for_db.Commands.check')
class CommandTests(SimpleTestCase):
    """Test the command"""

    def test_wait_for_db_ready(self, patched_check):
        """Test waiting for DB if DB is ready"""

        patched_check.return_value = True
        call_command('wait_for_db')

        patched_check.assert_called_once_with(databases=['default'])


