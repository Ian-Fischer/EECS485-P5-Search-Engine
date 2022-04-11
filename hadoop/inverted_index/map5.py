#!/usr/bin/env python3
"""MapReduce stage 5 map."""
import string
import sys
import json

if __name__ == "__main__":
    # mp5
    for line in sys.stdin:
        # parse the line
        line = line.split("\t")
        docid = line[0]
        d_i = line[1]
        # now, get all of the words
        word_dict_str = line[2]
        word_dict = json.loads(word_dict_str)
        # loop over all words and output "docid%3 word idfk docid di tf_ik"
        for word, info in word_dict.items():
            doc_info = {
                docid: [info[0], d_i]
            }
            sep = int(docid) % 3
            string_dct = json.dumps(doc_info)
            #        docid      word    idf_k      {docid: tf_ik, d_i}
            print(f"{sep}\t{word}\t{info[1]}\t{string_dct}")
