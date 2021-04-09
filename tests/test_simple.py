from django.test import TestCase

from apps.misc.views import add, subtract


class CalcTest(TestCase):

    def test_add_numbers(self):
        """Testing add method"""
        self.assertEqual(add(3,8), 11)

    def test_subtract_numbers(self):
        """Test subtract"""
        self.assertEqual(subtract(5,11), 6)
