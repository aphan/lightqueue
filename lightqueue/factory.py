import logging
from dispatcher import SequentialDispatcher, ParallelDispatcher


class Factory(object):
    # A Factory selects the correct dispatcher based on the execution model
    # (sequential or parallel processing)

    def __init__(self, multiprocessing=False, workers=4,
                 host='localhost', port=6379, db=0, queue_name='lightqueue'):

        logging.basicConfig(format='%(asctime)s %(message)s',
                            level=logging.DEBUG)

        # Choose either the Parallel or Sequential Dispatcher based on if
        # multiprocessing was enabled or not
        if multiprocessing:
            self.dispatcher = ParallelDispatcher(workers, host, port, db,
                                                 queue_name)
        else:
            self.dispatcher = SequentialDispatcher(host, port, db, queue_name)

        message = ('lightqueue started processing jobs on ' + host + ':' +
                   repr(port) + ', db ' + repr(db))

        if multiprocessing:
            message += ' (multiprocessing enabled)'
        logging.debug(message)

    def start(self):
        # Start the dispatcher
        self.dispatcher.dispatch()
