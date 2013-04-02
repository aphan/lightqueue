import logging
from queue import Queue
from dispatcher import Dispatcher, ParallelDispatcher


class Factory(object):

    def __init__(self, multiprocessing=False, max_workers=3, queue_name='lq'):
        self.queue = Queue(queue_name)
        logging.basicConfig(format='%(asctime)s %(message)s',
                            level=logging.DEBUG)

        if multiprocessing:
            self.dispatcher = ParallelDispatcher(max_workers)
        else:
            self.dispatcher = Dispatcher()

        logging.debug('Lightqueue started and listening for jobs')

    def work(self):
        while True:
                job = self.queue.dequeue()
                if type(self.dispatcher) == ParallelDispatcher:
                    while True:
                        # Check if the dispatcher is ready for another job
                        if self.dispatcher.ready_for_dispatch():
                            self.dispatcher.dispatch(job)
                            break
                else:
                    self.dispatcher.dispatch(job)
