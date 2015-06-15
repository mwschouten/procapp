__author__ = 'mathijs'

from hbsettings import Settings, NotValidError
from hbobjects import HbObject
import unittest


class test_settings(unittest.TestCase):
    def test_init(self):
        """ Initialisation should return Settings instance
        """
        t = Settings()
        self.assertIsInstance(t, Settings)

    def test_get_dependency(self):
        """ Can we retreive the dependencies?
        """
        t = Settings()
        t.add('aap', HbObject('test'), dependency=True)
        self.assertEqual(t.dependencies, ['aap'])

    def test_check_range(self):
        """ Setting something in allowed range
        """
        t = Settings()
        t.add('aap', 0, valid_range=[0, 10])
        t.set(aap=3)
        self.assertEqual(t.get['aap'], 3)
        t.set(aap=11)
        self.assertEqual(t.get['aap'], 0)


    def test_check_range(self):
        """ Setting something in allowed range
        """
        t = Settings()
        t.add('aap', 0, valid_range=[0, 10])
        self.assertRaises(NotValidError, t.set, aap=11)
        self.assertEqual(t.get['aap'], 0)

    def test_check_type(self):
        """ Setting wrong type
        """
        t = Settings()
        t.add('aap', 0, item_type=int)
        t.set(aap=3)
        self.assertEqual(t.get['aap'], 3)
        self.assertRaises(NotValidError, t.set, aap='banaan')

    def test_check_type_multiple(self):
        """ Various erroneous items
        """
        t = Settings()
        t.add('aap', 0, item_type=int)
        t.set(aap=[3, 4])
        self.assertItemsEqual(t.get['aap'], [3, 4])
        self.assertRaises(NotValidError, t.set, aap=[3, 'banaan'])


def main():
    unittest.main()


if __name__ == '__main__':
    main()

