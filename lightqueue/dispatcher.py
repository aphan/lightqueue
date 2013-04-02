import redis
from multiprocessing import Process


class Dispatcher(object):
    # A normal job dispatcher (no concurrency or parallelism)

    def dispatch(self, job):
        job.start(self)

    def job_finished(self, job_id):
        pass


class ParallelDispatcher(Dispatcher):
    # A job dispatcher that uses multiprocessing to dispatch jobs

    def __init__(self, max_workers):
        self.max_workers = max_workers
        self.db = redis.StrictRedis(host='localhost', port=6379, db=0)

        self.jobids_set = 'lq:jobids'
        self.db.delete(self.jobids_set)

    def ready_for_dispatch(self):
        return self.db.scard(self.jobids_set) < self.max_workers

    def dispatch(self, job):
        self.db.sadd(self.jobids_set, job.id)
        Process(target=job.start, args=(self,)).start()

    def job_finished(self, job_id):
        self.db.srem(self.jobids_set, job_id)
