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
        
        self.value = value[:value.rfind("/")-1]  ## Remove last "/"

        self.year  = None
        self.month = None
        self.day   = None
        
        self.process(self.value)
    def process(self, value):
        tokens = value.split("/")
        if len(tokens) > 3: raise ValueError("Date format allowed: Y, Y/M, Y/M/D. Value ="+self.value)
        if tokens[0] == "": raise TypeError("Invalid date - Must provide at least the year"+self.value)
        try:
            self.year = int(tokens[0])
            if len(tokens) > 1: self.month = int(tokens[1])
            if len(tokens) > 2: self.day   = int(tokens[2])
        except: pass

    def __str__(self):
        return self.value

    def __repr__(self):
        return self.__str__()
                                             

class citation(baseclass):
    def __init__(self, tokens):

        self.info = defaultdict(list)
        self.process(tokens)
    def process(self, tokens):

        for t in tokens:
            value = t[6:].rstrip()
            if value.strip()!= "":  ## No need of keys to empty values
                key = t[:4].strip() 
                if key in ["AU","KW"]: ## Author and Keyword can have n-values
                    self.info[key].append(value)
                else: 
                    self.info[key] = value
                if key == "PY":
                    self.info[key] = dateclass(value)
    def getvalue(self,key):
        return self.info.get(key)

def readbiblio(filename):
    
    ## Open the file in universal mode
    with open(filename,"rU") as f:
        tokens = []
        ## Loop the file...
        for index,line in enumerate(f,start=1):
            ## Add the lines to temporarly list until 
            ## it find a return line feed
            if line != f.newlines:
                tokens.append(line)
            elif tokens:
                ## If the token is not empty yield a citation
                yield citation(tokens)
                tokens = []
        print "Processed", index, "lines"

def main():
    pubyear = defaultdict(int)
    filename = "data/bigdata.all.ris"
    for c in readbiblio(filename):
        p = c.getvalue("PY") 
        if p and p.year >= 2007: 
            pubyear[p.year] += 1

        #print index, c.getvalue("PY")
        #print c.getvalue("T1"), "\nAuthors:" + str(c.getvalue("AU")) , "\r\nKeywords:" + str(c.getvalue("KW"))
    for k,v in pubyear.items():
        print k,v
    #print pubyear

if __name__ == "__main__":
    main()
        
