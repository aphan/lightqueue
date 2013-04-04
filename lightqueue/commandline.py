import argparse
from lightqueue.factory import Factory


def start():
    parser = argparse.ArgumentParser()

    parser.add_argument('command')

    parser.add_argument('-e', action='store', dest='execution',
                        default='sequential',
                        help='execution model (sequential or parallel)')

    parser.add_argument('-workers', action='store', dest='workers', type=int,
                        default=4,
                        help='# of jobs processed at a time (for -e parallel)')

    parser.add_argument('-host', action='store', dest='host',
                        default='localhost',
                        help='redis server\'s hostname')

    parser.add_argument('-port', action='store', dest='port', type=int,
                        default=6379, help='redis server\'s port')

    parser.add_argument('-db', action='store', dest='db', type=int,
                        default=0, help='redis server\'s db')

    parser.add_argument('-qname', action='store', dest='queue_name',
                        default='lightqueue',
                        help='lightqueue namespace in Redis db')

    parser.add_argument('--version', action='version',
                        version='%(prog)s 0.1.0')

    # Parse the command
    results = parser.parse_args()

    if results.command == 'start':

        multiprocessing = False
        if results.execution == 'parallel':
            multiprocessing = True

        Factory(multiprocessing=multiprocessing,
                workers=results.workers,
                host=results.host,
                port=results.port,
                db=results.db,
                queue_name=results.queue_name).start()
    else:
        print 'Use "lightqueue start" to start processing jobs'
