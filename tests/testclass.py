class TestClass(object):

    def overwrite(self, filename, str):
        f = open(filename, 'w+')
        f.write(str)
        f.close()
