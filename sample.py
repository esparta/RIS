from __future__ import print_function 
from risparser import RISParser
from collections import defaultdict

def main():
    pubyear = defaultdict(int)
    filename = "data/hadoop-mapreduce.ris"

    with RISParser(filename) as citations:
        for c in citations:
            p = c.getvalue("PY")
            #print c.getvalue("AU")    
            pubyear[p.year] += 1

    refs = 0
    for k,v in pubyear.items():
        print(k,v)
        refs += v

    print("Total references: {0}".format(refs))
    #print pubyear

if __name__ == "__main__":
    main()

