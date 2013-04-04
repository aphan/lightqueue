import signal
import sys
from queue import Queue


class Worker(object):

    def __init__(self, queue_name):
        self.queue = Queue(queue_name)
        self.current_pickled_job = None

        # Register handlers for SIGINT and SIGTRM
        signal.signal(signal.SIGINT, self.handle_exit)
        signal.signal(signal.SIGTERM, self.handle_exit)

    def work(self):
        while True:

            job_tuple = self.queue.dequeue()

            if job_tuple is not None:
                self.current_pickled_job, job = job_tuple
                job.start(self)

    def job_finished(self, job_id):
        self.current_pickled_job = None

    def handle_exit(self, signal, frame):
        if self.current_pickled_job is not None:
            self.queue.add_pickled_jobs_to_front(self.current_pickled_job)
        sys.exit()
