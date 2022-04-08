#!/usr/bin/env python3
import sys
import json
import itertools
from reduce0 import keyfunc

if __name__ == "__main__":
    # now we just need to get the final output
    for key, group in itertools.groupby(sys.stdin, keyfunc):
        # for the one line in each group, calc w_ik
        for line in group:
            # split the line up
            line = line.split("\t")
            # dictionary
            dict_str = line[2]
            dictionary = json.loads(dict_str)
            # idf_k
            idf_k = float(line[1])
            # iterate over and calculate
            for docid, value in dictionary.items():
                # tf_ik, add wik
                dictionary[docid].append((float(value[0])*idf_k)**2)
        finaldct_str = json.dumps(dictionary, sort_keys=True)
        print(f"{key}\t{idf_k}\t{finaldct_str}")
