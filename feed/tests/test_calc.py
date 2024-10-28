"""
Test custom Django management commands.
"""
from django.test import SimpleTestCase


class CalcTests(SimpleTestCase):
    """Test commands."""

    def test_wait_for_db_ready(self):
        """Test waiting for database if database ready."""

        res = 11

        self.assertEqual(res, 11)
