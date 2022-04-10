#!/usr/bin/env python3
import sys
import json
import itertools
from heapq import merge
from reduce0 import keyfunc

def keyfunc2(line):
    """Return the key from a TAB-delimited key-value pair."""
    return line.split("\t")[1]

if __name__ == "__main__":
    # separate by docid % 3
    for key, group in itertools.groupby(sys.stdin, keyfunc):
        # separate by the word
        #   key    list of words
        for word, info in itertools.groupby(group, keyfunc2):
            # go through all the words in this separation
            docids_dict = {}
            idf_k = 0
            for line in info:
                # partition the line
                line = line.split("\t")
                docid_dict = json.loads(line[3])
                docids_dict.update(docid_dict)
                idf_k = line[2]
            output_string = ""
            for key in sorted(docids_dict):
                tf_ik = docids_dict[key][0]
                mag_d_i = docids_dict[key][1]
                output_string = output_string+f" {key} {tf_ik} {mag_d_i}"
            print(f"{word} {idf_k}"+output_string)
            
            