

class baseclass(object):
    def __init__(self):
        self.name = ""


class dateclass(baseclass):
    
    def __init__(self,value):
        if not isinstance(value, str) : raise TypeError("value for dateclass param is string")
        
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

        self.info = {}
        self.process(tokens)
    def process(self, tokens):

        for t in tokens:
            value = t[6:].rstrip()
            if value.strip()!= "":  ## No need of keys to empty values
                key = t[:4].strip() 
                if key in ["AU","KW"]: ## Author and Keyword can have n-values
                    ## if we don't have this keys, add it
                    if self.info.get(key) == None : 
                        self.info[key] = [value]
                    else: self.info[key].append(value) ## or append the value
                else: self.info[key] = value
                if key == "PY":
                    self.info[key] = dateclass(value)
    def getvalue(self,key):
        return self.info.get(key)

def readbiblio():
    citations  = []
    with open("bigdata.exact_journals.ris") as f:
        tokens = []
        for index,line in enumerate(f):
           if line != "\r\n":
              tokens.append(line)
           elif len(tokens) > 0:
               citations.append(citation(tokens))
               tokens = []
        print "Processed", index, "lines"
    pubyear = {}
    for index, c in enumerate(citations,1):
        p = c.getvalue("PY") 
        if p != None and p.year >= 2007: 
            key = p.year 
            if pubyear.get(key) == None:
              pubyear[key] = 1
            else:  
                pubyear[key] += 1

        #print index, c.getvalue("PY")
        #print c.getvalue("T1"), "\nAuthors:" + str(c.getvalue("AU")) , "\r\nKeywords:" + str(c.getvalue("KW"))
    for index,y in enumerate(pubyear):
        print y, pubyear[y]
    print pubyear
readbiblio()
        
