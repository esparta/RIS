"""
risparser
Module to process a the bibliographic file format called RIS.
"""
from collections import defaultdict
import re

TITLE_REGEX = re.compile(r"(.*?)\s*-\s*(.*)")

class Dateclass(object):
    """ Utility class for date manipulation """
    def __init__(self, value):
        ## Can handle only str or unicode
        if not isinstance(value, basestring):
            message = """
                dateclass: Value param must be str or unicode. Suplied:{}
            """
            raise TypeError(message.format(type(value)))

        ## Remove last "/" if suplied
        self.value = value[:value.rfind("/") - 1]
        self.year  = None
        self.month = None
        self.day   = None
        ## process only non-empty values
        if value.rstrip():
            self.process(self.value)
    def process(self, value):
        """ Process the date """
        tokens = value.split("/")
        if len(tokens) > 3:
            message = "Date format allowed: Y, Y/M, Y/M/D. Value = {value}"
            raise ValueError(message.format(value=self.value))
        try:
            self.year = int(tokens[0])
            if len(tokens) > 1:
                self.month = int(tokens[1])
            if len(tokens) > 2:
                self.day   = int(tokens[2])
        except ValueError:
            pass

    def get_year(self):
        """ Return the processed year """
        return self.year

    def __str__(self):
        return self.value

    def __repr__(self):
        return self.__str__()


class Citation(object):
    """ Class to process a citation """
    def __init__(self, tokens):
        """ Initialize the class """
        self.info = defaultdict(list)
        self.process(tokens)
    def process(self, tokens):
        """ Process the file """
        for token in tokens:
            __key, __value = TITLE_REGEX.search(token).groups()
            ## Author and Keyword can have n-values
            if __key in ["AU","KW"]:
                self.info[__key].append(__value)
            else:
                self.info[__key] = __value
            if __key == "PY":
                self.info[__key] = Dateclass(__value)

    def getvalue(self, key):
        """ obtain a given value from the dictionary """
        return self.info.get(key)

from contextlib import contextmanager

@contextmanager
def risparser(filename):
    """ Process the RIS file """
    yield readbiblio(filename)

def readbiblio(filename):
    """ Read a RIS file """
    ## Open the file in universal mode
    with open(filename,"r") as __file:
        __tokens = []
        ## Loop the file...
        for __line in __file:
            __line = __line.rstrip()
            ## Add the lines to temporarly list until
            ## it find the End of Reference, ignoring the line feed
            if __line:
                if __line[:2] != "ER":
                    __tokens.append(__line)
                elif __tokens:
                    ## If the token is not empty yield a citation
                    yield Citation(__tokens)
                    __tokens = []

