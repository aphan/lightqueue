import logging
import time
from func import Func


class Job(object):

    def __init__(self, id, func, args):
        self.id = id
        self.func = Func(func, args, self)

    def start(self, dispatcher):
        self.dispatcher = dispatcher

        logging.debug('Started Job #' + repr(self.id))
        self.start_time = time.time()

        self.func.execute()

    def finished_successfully(self):
        logging.debug('Finished Job #' + repr(self.id) + '; took ' +
                      repr(time.time() - self.start_time) + ' seconds')
        self.dispatcher.job_finished(self.id)

    def failed(self, error_str):
        logging.debug('>>>>> Job #' + repr(self.id) + ' failed; ' +
                      repr(error_str))
        self.dispatcher.job_finished(self.id)
