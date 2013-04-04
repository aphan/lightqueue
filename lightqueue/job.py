import logging
import time
from func import Func


class Job(object):
    # A job stores the representation of the function that is to be executed.

    def __init__(self, id, func, args, kwargs):
        self.id = id
        self.func = Func(func, args, kwargs, self)

    def start(self, worker, is_parent_process=True):
        # This function is called by the worker who dequeued it from the queue.
        self.worker = worker
        logging.debug('Started Job #' + repr(self.id))
        self.start_time = time.time()

        # Execute the function
        self.func.execute()

    def finished_successfully(self):
        # Log that this job successfuly finished and tell the worker that this
        # job completed

        logging.debug('Finished Job #' + repr(self.id) + '; took ' +
                      repr(time.time() - self.start_time) + ' seconds')
        self.worker.job_finished(self.id)

    def failed(self, error_str):
        # Log the error and tell the worker that this job completed

        logging.debug('>>>>> Job #' + repr(self.id) + ' failed; ' +
                      repr(error_str))
        self.worker.job_finished(self.id)
