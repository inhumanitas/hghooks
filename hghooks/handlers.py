import sys

class OutHandler(object):
    def __init__(self, sys):

        self.stdout = sys.stdout
        sys.stdout = self
        self.__log = []
        self.path_delim = 'src'
        self.log_limit = 10

    def write(self, text):
        if text.strip() and (self.log_limit > len(self.__log)):
            head, delimeter, tail = text.partition(self.path_delim)
            logging_str = tail if tail else head
            self.__log.append(logging_str)

    def get_log(self, sep='\n'):
        self.__log.insert(0, "Showing first %d messages" % self.log_limit)
        return str(sep).join(self.__log)

    def close(self):
        sys.stdout = self.stdout


class SysOutHandler(object):
    u"""This context manager captures all system output to self list"""
    def __init__(self, sys, log_limit=10):
        self.__stdout = sys.stdout
        sys.stdout = self
        self.__log = []
        self.path_delim = 'src'
        self.__log_limit = log_limit

    def __enter__(self):
        return self

    def filtered(self, text):
        u"""Additional filter to prociding text
        Override this function to change filter behavior
        :returns: boolean context
        """
        return text.strip()

    def write(self, text):
        if self.filtered(text) and (self.__log_limit > len(self.__log)):
            head, delimeter, tail = text.partition(self.path_delim)
            logging_str = tail if tail else head
            self.__log.append(logging_str)

    def get_log(self, sep='\n'):
        self.__log.insert(0, "Showing first %d messages" % self.__log_limit)
        return str(sep).join(self.__log)

    def __close(self):
        sys.stdout = self.__stdout

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__close()


def test_out_hadler():
    out =  OutHandler(sys)

    print ">>> 123"
    print ">>> main is runned"
    out.close()
    print "Saved log:",
    print out.get_log()


def test_sys_out_hadler():
    with SysOutHandler(sys) as out:
        print ">>> 123"
        print ">>> main is runned"
        log = out.get_log()

    print "Saved log:",
    print log


if __name__ == "__main__":
    test_out_hadler()
    test_sys_out_hadler()
