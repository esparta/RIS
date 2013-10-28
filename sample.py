from risparser import RISParser
from collections import defaultdict

def main():
    pubyear = defaultdict(int)
    filename = "data/bigdata.keyword.ris"

    with RISParser(filename) as citations:
        for c in citations:
            p = c.getvalue("PY")
            print c.getvalue("AU")
            if p and p.year != None:     
                pubyear[p.year] += 1

    for k,v in pubyear.items():
        print k,v
    #print pubyear

if __name__ == "__main__":
    main()

