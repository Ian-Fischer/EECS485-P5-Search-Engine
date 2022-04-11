#!/usr/bin/env python3
"""MapReduce stage 3 map."""
import sys
import json
import math

if __name__ == "__main__":
    # get the total number of documents
    with open("total_document_count.txt", "r", encoding="utf-8") as file:
        N = int(file.read())
    # nk is the third element in line
    for line in sys.stdin:
        # now, we will go through each reduce output
        # each line is word\t{sorted dict}\tn_k
        info = line.split("\t")
        # get the information from the line
        key = info[0]
        # get the dictionary from the dumps
        dict_str = info[1]
        tf_iks = json.loads(dict_str)
        n_k = int(info[2])
        # idfk = log_10(N/n_k)
        d_i = 0
        idf_k = math.log10(N/n_k)
        altered_dict_str = json.dumps(tf_iks, sort_keys=True)
        print(f"{key}\t{idf_k}\t{altered_dict_str}")
