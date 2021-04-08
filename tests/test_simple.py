from django.test import TestCase

from apps.misc.views import add


class CalcTest(TestCase):

    def test_add_numbers(self):
        """Testing add method"""
        self.assertEqual(add(3,8), 11)
