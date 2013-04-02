import unittest
import time
import redis
from lightqueue.queue import Queue
from tests.testclass import TestClass


class TestLightqueue(unittest.TestCase):

    def setUp(self):
        self.queue = Queue('lqtest')

    def tearDown(self):
        db = redis.StrictRedis(host='localhost', port=6379, db=0)
        db.delete('lqtest')
        db.delete('lqtest:incr')

    def test_queue_instance_method(self):
        t = TestClass()
        self.queue.enqueue(t.overwrite, 'test_file.txt', 'test string')

        # wait for the job to complete
        time.sleep(3)

        f = open('test_file.txt', 'r')
        self.assertEqual(f.read(), 'test string')
        f.close()

if __name__ == '__main__':
    unittest.main()
