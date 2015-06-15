from hbtasks_v2 import HbTask
from hbobjects import HbObject
import unittest


class test_tasks(unittest.TestCase):
    def test_init(self):
        t = HbTask()
        self.assertIsInstance(t, HbTask)

    def test_requires_one(self):
        """ Make sure the tasks gives its required dependencies
        """
        t = HbTask()
        t.settings.add('aap', HbObject('test'), dependency=True)
        self.assertEqual(t.dependencies,['aap'])

    def test_requires_known_object(self):
        """
        """
        def make(self):
            self.content='That was easy'

        o = HbObject('banaan', make=make)
        t = HbTask()
        # task needs the object to be ready
        t.settings.add('aap', o, dependency=True)
        # first, not ready
        self.assertFalse(t.ready_to_go)
        # then prepare
        print o.__dict__
        o.get()
        # and now be ready
        self.assertTrue(t.ready_to_go)


    def test_tell_me_what_to_do(self):
        """
        """
        o = HbObject('banaan')
        t = HbTask()
        # task needs the object to be ready
        t.settings.add('aap', o, dependency=True)
        # first, not ready
        self.assertFalse(t.ready_to_go)
        # then prepare
        print 'Todo: ',t.todos

