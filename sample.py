""" Functional testing file. Sample some features on risparser"""
# -*- coding: utf-8 -*-
from __future__ import print_function
from risparser import risparser
from collections import defaultdict
import optparse
import sys
import time

def main(args=None):
    """ Functional testing file """
    ## Set up option parser
    parser = optparse.OptionParser(usage="python sample.py [options] file")
    parser.add_option("-v", "--verbose", action="store_true",
                      help="Verbose logging", default=False)

    options, args = parser.parse_args(args)
    if not args:
        sys.stderr.write("Need at least a file to process\n")
        sys.stderr.write("Use --help to show usage\n")
        return 2

    ## for every file in args
    for filename in args:
        pubyear = defaultdict(int)

        print("Processing {0}".format(filename))
        if options.verbose:
            init_time = time.time()
        with risparser(filename) as citations:
            for cite in citations:
                publication = cite.getvalue("PY")
                pubyear[publication.year] += 1


        refs = 0

        for key, value in pubyear.items():
            print(key, value)
            refs += value

        if options.verbose:
            print("Total references: {r} on {s:.2} seconds"\
                  .format(r=refs, s = time.time() - init_time))

if __name__ == "__main__":
    main()

