import pickle
import redis
from job import Job


class Queue(object):

    def __init__(self, queue_name='lq'):
        self.db = redis.StrictRedis(host='localhost', port=6379, db=0)
        self.queue_name = queue_name

    def enqueue(self, func, *args):
        job = Job(self.generate_job_id(), func, args)
        pickled_job = pickle.dumps(job)
        self.db.lpush(self.queue_name, pickled_job)

    def dequeue(self):
        pickled_job = self.db.brpop(self.queue_name)[1]
        return pickle.loads(pickled_job)

    def generate_job_id(self):
        return self.db.incr(self.queue_name + ':incr')
