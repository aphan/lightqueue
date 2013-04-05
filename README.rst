===========
lightqueue
===========

lightqueue is a lightweight job queue that processes jobs (Python
function calls) from a queue located inside a Redis database.
There is also support for processing multiple jobs at once.

To install it:

::

    $ pip install lightqueue

After you have lightqueue (and Redis) installed, you are ready to start queueing jobs.
Say you have a function like this in a module called **mymodule**

::

    def myfunc(num):
      print sum([x for x in range(num)])

To add the execution of this function as a job into lightqueue:

::

    >>> from lightqueue.queue import Queue
    >>> from mymodule import myfunc
    >>> q = Queue()
    >>> q.enqueue(myfunc, 9999) # add the job myfunc(9999) to the queue
    >>> q.enqueue(myfunc, 1234567) # add the job myfunc(1234567) to the queue

To start processing these jobs, type this in a shell prompt:

::

    $ lightqueue start


If the lightqueue process has to shut down in the middle of executing the job,
it will place the job back onto the front of the queue.


Change db server
--------------------

By default, lightqueue adds jobs to and processes jobs from the Redis server
located at localhost:6379 on db=0.  To change any of these settings:

::

    >>> Queue q = Queue(host='myredishost', port=7323, db=4)

Then give the lightqueue process the same settings:

::

    $ lightqueue start -host myredishost -port 7323 -db 4


Parallel Processing
--------------------

By default, lightqueue processes one job from the queue at a time.
To process more than one job at once (let's say 4), start up lightqueue
with the following command-line args:


::

    $ lightqueue start -e parallel -workers 4

This uses the Python multiprocessing module so be aware of all of the usual
caveats of parallel processing.
