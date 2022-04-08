#!/usr/bin/env python3
import sys
import json


if __name__ == "__main__":
    # mr4
    for line in sys.stdin:
        # parse the line
        line = line.partition("\t")
        word = line[0]
        idf_k = line[2]
        #dictionary
        docid_dict_str = line[4]
        docid_dict = json.loads(docid_dict_str)
        # {docid: tfik, wik}
        # now map the line to many lines, word info is tfik and wik
        for docid, word_info in docid_dict.items():
            # print docid \t w_ik \t {word: [tf_ik, idf_k]}
            w_ik = word_info[1]
            word_info[1] = idf_k
            word_dict_str = json.dumps(word_info, sort_keys=True)
            print(f"{docid}\t{w_ik}\t{word_dict_str}")

        """
        word   idfk     {docid1{tfik, wik}, docid2{tfik, wik}, ..., docidn}

        -->

        docid1    wik    {word: tfik, idfk}
        ...
        docidn    wik    {word: tfik, idfk}
    
        """