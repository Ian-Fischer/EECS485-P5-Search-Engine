#!/usr/bin/env python3
from heapq import merge
import sys
import json
import itertools
from hadoop.inverted_index.reduce0 import keyfunc

if __name__ == "__main__":
    # now, reduce
    """
    reduce by docid
    sum all w_ik's pulled out in map4
    concat all dicts so we have all the words in that document
    now that we know the doc, we know where to print the words
    """
    for key, group in itertools.groupby(sys.stdin, keyfunc):
        sum_wik = 0
        words_dict = {}
        for line in group:
            # partition the line
            line = line.partition("\t")
            docid = line[0]
            w_ik = line[2]
            sum_wik += w_ik
            # merge all the dictionaries
            word_dict = json.loads(line[4])
            words_dict = merge(words_dict, word_dict)
        words_dict_str = json.dumps(words_dict, sort_keys=True)
        print(f"{docid}\t{sum_wik}\t{words_dict_str}")