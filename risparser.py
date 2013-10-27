from collections import defaultdict

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

        self.info = defaultdict(list)
        self.process(tokens)
    def process(self, tokens):

        for t in tokens:
            value = t[6:].rstrip()
            if value.strip()!= "":  ## No need of keys to empty values
                key = t[:4].strip() 
                if key in ["AU","KW"]: ## Author and Keyword can have n-values
                   self.info[key].append(value)
                else: self.info[key] = value
                if key == "PY":
                    self.info[key] = dateclass(value)
    def getvalue(self,key):
        return self.info.get(key)

def readbiblio():
    citations  = []
    ## Open the file in universal mode
    with open("data/bigdata.keyword.ris","rU") as f:
        tokens = []
        ## Loop the file...
        for index,line in enumerate(f):
            ## Add the lines to temporarly list until 
            ## it find a return line feed
            if line != f.newlines:
                tokens.append(line)
            elif tokens:
                ## If the token is not empty add a citation
                citations.append(citation(tokens))
                tokens = []
        print "Processed", index, "lines"
    pubyear = {}
    for index, c in enumerate(citations,1):
        #print c.getvalue("T1")
        p = c.getvalue("PY") 
        if p and p.year >= 2007: 
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

if __name__ == "__main__":
   readbiblio()
        
