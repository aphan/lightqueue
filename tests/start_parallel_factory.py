from lightqueue.factory import Factory

Factory(multiprocessing=True, queue_name='lqtest').work()
