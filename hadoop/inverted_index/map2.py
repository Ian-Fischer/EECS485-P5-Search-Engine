#!/usr/bin/env python3
import sys
import json

if __name__ == "__main__":
    # go through each line
    # string is
    for line in sys.stdin:
        # for each word, output word \t doc_id #
        # first, split over the tabs
        row = line.partition("\t")
        # docid_word
        key = row[0]
        # split the key
        docid = key.split("_")[0]
        word = key.split("_")[1]
        # word frequency in given docid
        word_frq = row[1]
        # now we have docid, word, word frequency
        output_dict = {
            docid: [word_frq]
        }
        # get the dictionary as a string
        output_string = json.dumps(output_dict)
        # print word \t {docid: word_freq}
        print(f"{word}\t{output_string}")