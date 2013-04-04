import unittest
import time
import redis
from lightqueue.queue import Queue
from tests.testclass import TestClass


class TestParallelLightqueue(unittest.TestCase):

    def setUp(self):
        self.queue = Queue('lqtest')
        self.filename = 'test_file.txt'

    def tearDown(self):
        db = redis.StrictRedis(host='localhost', port=6379, db=0)
        db.delete('lqtest')
        db.delete('lqtest:incr')

    def test_queue_instance_methods(self):
        open(self.filename, 'w').close()
        t = TestClass()

        self.queue.enqueue(t.write, self.filename, '1')
        self.queue.enqueue(t.write, self.filename, '2')
        self.queue.enqueue(t.write, self.filename, '3')
        self.queue.enqueue(t.write, self.filename, '4')
        self.queue.enqueue(t.write, self.filename, '5')

        # wait for the jobs to complete
        time.sleep(3)

        f = open(self.filename, 'r')
        self.assertEqual(set(list(f.read())), set(list('12345')))
        f.close()


if __name__ == '__main__':
    unittest.main()
