import signal
import sys
from queue import Queue


class Worker(object):
    # A worker dequeues and executes jobs from the queue

    def __init__(self, host, port, db, queue_name):
        self.queue = Queue(host, port, db, queue_name)
        self.current_pickled_job = None

        # Register handlers for SIGINT and SIGTERM
        signal.signal(signal.SIGINT, self.handle_exit)
        signal.signal(signal.SIGTERM, self.handle_exit)

    def work(self):
        while True:
            # Block until a job can be dequeued from the queue. Then execute it

            job_tuple = self.queue.dequeue()

            if job_tuple is not None:
                self.current_pickled_job, job = job_tuple
                job.start(self)

    def job_finished(self, job_id):
        self.current_pickled_job = None

    def handle_exit(self, signal, frame):
        # When the program has to shutdown before the current job is done
        # executing, add it back to the front of the queue.

        if self.current_pickled_job is not None:
            self.queue.add_pickled_jobs_to_front(self.current_pickled_job)

        sys.exit()
