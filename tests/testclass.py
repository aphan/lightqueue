class TestClass(object):

    def write(self, filename, str):
        f = open(filename, 'a')
        f.write(str)
        f.close()
