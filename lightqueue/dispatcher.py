# import redis
from multiprocessing import Process
# from queue import Queue
from worker import Worker


class SequentialDispatcher(object):
    # Only one worker; jobs are pulled off the queue one at a time and
    # processed sequentially.

    def __init__(self, queue_name):
        self.queue_name = queue_name

    def dispatch(self):
        # Create a single worker
        Worker(self.queue_name).work()


class ParallelDispatcher(object):
    # Use multiprocessing to launch worker processes

    def __init__(self, queue_name, max_workers):
        self.queue_name = queue_name
        self.max_workers = max_workers

    def dispatch(self):
        # Create a new process for each worker
        for x in range(self.max_workers):
            Process(target=Worker(self.queue_name).work).start()
