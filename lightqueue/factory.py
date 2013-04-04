import logging
from dispatcher import SequentialDispatcher, ParallelDispatcher


class Factory(object):
    # A Factory selects the correct dispatcher based on the execution model
    # (sequential or parallel processing)

    def __init__(self, multiprocessing=False, max_workers=2, queue_name='lq'):
        logging.basicConfig(format='%(asctime)s %(message)s',
                            level=logging.DEBUG)

        # Choose either the Parallel or Sequential Dispatcher based on if
        # multiprocessing was enabled or not
        if multiprocessing:
            self.dispatcher = ParallelDispatcher(queue_name, max_workers)
        else:
            self.dispatcher = SequentialDispatcher(queue_name)

        message = 'Lightqueue started and listening for jobs'
        if multiprocessing:
            message += ' (multiprocessing enabled)'
        logging.debug(message)

    def start(self):
        # Start the dispatcher
        self.dispatcher.dispatch()
