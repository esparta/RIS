from collections import defaultdict

class baseclass(object):
    def __init__(self):
        self.name = ""


class dateclass(baseclass):
    
    def __init__(self,value):
        if not (isinstance(value, str) \
            or isinstance(value, unicode)): 
            raise TypeError("value paramt must be string / unicode.\
                             Suplied:{}".format(type(value)))
        
        ## Remove last "/" if suplied
        self.value = value[:value.rfind("/")-1]  

        self.year  = None
        self.month = None
        self.day   = None
        ## process only non-empty values
        if value.rstrip():
            self.process(self.value)
    def process(self, value):
        tokens = value.split("/")
        if len(tokens) > 3: 
            raise ValueError("Date format allowed: Y, Y/M, Y/M/D. Value ="+self.value)
        try:
            self.year = int(tokens[0])
            if len(tokens) > 1: 
                self.month = int(tokens[1])
            if len(tokens) > 2: 
                self.day   = int(tokens[2])
        except: pass

    def __str__(self):
        return self.value

    def __repr__(self):
        return self.__str__()
                                             

class __citation(baseclass):
    def __init__(self, tokens):

        self.info = defaultdict(list)
        self.process(tokens)
    def process(self, tokens):

        for t in tokens:
            __dash = t.find("-")
            __key = t[:__dash].rstrip()
            __value = t[__dash+1:].lstrip()
            ## Author and Keyword can have n-values
            if __key in ["AU","KW"]: 
                self.info[__key].append(__value)
            else: 
                self.info[__key] = __value
            if __key == "PY":
                self.info[__key] = dateclass(__value)

    def getvalue(self,key):
        return self.info.get(key)

from contextlib import contextmanager

@contextmanager
def RISParser(filename):
    yield readbiblio(filename)

def readbiblio(filename):
    
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
                    yield __citation(__tokens)
                    __tokens = []

