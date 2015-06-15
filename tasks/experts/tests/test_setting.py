from unittest import TestCase

from hbsettings import Setting, NotValidError

__author__ = 'mathijs'

class TestSetting(TestCase):

    def test_init(self):
        """ initialize a setting
        """
        q = Setting('banaan','geel')
        self.assertIsInstance(q,Setting)

    def test_init_not_mandatory(self):
        """ initialize not as mandatory setting
        """
        q = Setting('banaan', 'geel')
        self.assertFalse(q.mandatory)

    def test_init_as_mandatory(self):
        """ initialize a setting as mandatory
        """
        q = Setting('banaan', 'geel', mandatory=True)
        self.assertTrue(q.mandatory)

    def test_init_not_dependency(self):
        """ initialize a setting not as dependency
        """
        q = Setting('banaan', 'geel')
        self.assertFalse(q.dependency)

    def test_init_as_dependency(self):
        """ initialize a setting as dependency
        """
        q = Setting('banaan', 'geel', dependency=True)
        self.assertTrue(q.dependency)

    def test_validate_above_range(self):
        """ test set outside valid range
        """
        q = Setting('banaan', 'geel', valid_range=[0, 1])
        self.assertRaises(NotValidError, q.set, 2)

    def test_validate_below_range(self):
        """ test set outside valid range
        """
        q = Setting('banaan', 'geel', valid_range=[0, 1])
        self.assertRaises(NotValidError, q.set, -0.1)

    def test_validate_not_even_near_range1(self):
        """ test valid range with inappropriate offer
        """
        q = Setting('banaan', 'geel', valid_range=[2, 3])
        self.assertRaises(NotValidError, q.set, True)

    def test_validate_not_even_near_range2(self):
        """ test valid range with inappropriate offer
        """
        q = Setting('banaan', 'geel', valid_range=[0, 1])
        self.assertRaises(NotValidError, q.set, {'a': 1})

    def test_validate_not_even_near_range3(self):
        """ test valid range with inappropriate offer
        """
        q = Setting('banaan', 'geel', valid_range=[0, 1])
        self.assertRaises(NotValidError, q.set, 'fiets')

    def test_validate_range_ok(self):
        """ test set ok in valid range
        """
        q = Setting('banaan', 'geel', valid_range=[0, 1])
        q.set(0.5)
        self.assertEqual(q.validate(0.5), 0.5)

    def test_validate_range_ok_on_edge(self):
        """ test set ok on edge of valid range
        """
        q = Setting('banaan', 'geel', valid_range=[0, 1])
        self.assertEqual(q.validate(1), 1)
        self.assertEqual(q.validate(0), 0)


    def test_validate_valid_set(self):
        """ test set not in valid set
        """
        q = Setting('banaan', 'geel', valid_set=['geel','rood'])
        self.assertRaises(NotValidError, q.set, 'groen')


    def test_validate_valid_set_capital(self):
        """ test set not in valid set (capitals do matter)
        """
        q = Setting('banaan', 'geel', valid_set=['geel', 'rood'])
        self.assertRaises(NotValidError, q.set, 'Rood')


    def test_validate_valid_set_ok(self):
        """ test set ok in valid set (capitals do matter)
        """
        q = Setting('banaan', 'geel', valid_set=['geel', 'rood'])
        self.assertEqual(q.validate('rood'), 'rood')

    def test_validate_set_ok(self):
        """ test set ok in valid range
        """
        q = Setting('banaan', 'geel', valid_range=[0, 1])
        q.set(0.5)
        self.assertEqual(q.value, 0.5)


    def test_validate_multiple1(self):
        """ test set ok in valid range
        """
        q = Setting('banaan', 'geel', valid_range=[0, 1])
        self.assertRaises(NotValidError, q.set, [0.1, 0.2, 0.3, 1.1])


    def test_check(self):
        pass