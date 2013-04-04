import pickle
import sys
import redis
from job import Job


class Queue(object):
    # A queue has the responsibility to queue and dequeu jobs from the database

    def __init__(self, queue_name='lq'):
        self.db = redis.StrictRedis(host='localhost', port=6379, db=0)
        self.queue_name = queue_name

    def enqueue(self, func, *args):
        # Create a job object to hold the function. Then pickle the job object
        # and place it at the end of the queue.

        job = Job(self.generate_job_id(), func, args)
        pickled_job = pickle.dumps(job)
        self.db.lpush(self.queue_name, pickled_job)

    def dequeue(self):
        # Remove a pickled job from the front of the queue.  If the queue is
        # empty, block until an item is available.

        try:
            pickled_job = self.db.brpop(self.queue_name)[1]
            return (pickled_job, pickle.loads(pickled_job))
        except KeyboardInterrupt:
            sys.exit()

    def add_pickled_jobs_to_front(self, *pickled_jobs):
        # Add a pickled job to the front of the queue.

        self.db.rpush(self.queue_name, *pickled_jobs)

    def generate_job_id(self):
        return self.db.incr(self.queue_name + ':incr')
