import time
import random


class TestClass(object):

    def write(self, filename, str):
        time.sleep(random.random())

        f = open(filename, 'a')
        f.write(str)
        f.close()
