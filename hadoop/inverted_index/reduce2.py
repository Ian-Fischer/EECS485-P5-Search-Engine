#!/usr/bin/env python3
import sys
import json
import itertools
from inverted_index.reduce0 import keyfunc

if __name__ == "__main__":
    # now, we need to reduce based of word
    for key, group in itertools.groupby(sys.stdin, keyfunc):
        new_dict = {}
        for line in group:
            # get the json string
            in_dict = json.loads(line.partition("\t")[2])
            # load into a dict and merge with new_dict
            new_dict = new_dict.merge(new_dict, in_dict)
        # once we are done with this key, dumps
        new_dict_str = json.dumps(new_dict, sort_keys=True)
        # output is word \t {sorted dictionary of tf_ik's} n_k
        print(f"{key}\t{new_dict_str}\t{len(new_dict)}")
