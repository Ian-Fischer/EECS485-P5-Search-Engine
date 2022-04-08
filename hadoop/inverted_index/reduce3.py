#!/usr/bin/env python3
import sys
import json
import itertools
from inverted_index.reduce0 import keyfunc

if __name__ == "__main__":
    # now we just need to get the final output
    for key, group in itertools.groupby(sys.stdin, keyfunc):
        # for the one line in each group, calc w_ik
        for line in group:
            # split the line up
            line = line.partition("\t")
            # dictionary
            dict_str = line[4]
            dictionary = json.loads(dict_str)
            # idf_k
            idf_k = line[2]
            # iterate over and calculate
            for key, value in dictionary:
                # tf_ik, add wik
                dictionary[key].append((value*idf_k)**2)
        finaldct_str = json.dumps(dictionary, sort_keys=True)
        print(f"{key}\t{idf_k}\t{finaldct_str}")
