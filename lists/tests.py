from django.test import TestCase

class SmokeTest(TestCase):
    '''Failure expected'''

    def test_bad_maths(self):
        assertEquals(1 + 1, 3)
