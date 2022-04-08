#!/usr/bin/env python3
"""Map 1."""
import sys
import re
import csv

if __name__ == "__main__":
    for line in sys.stdin:
        # set csv max size
        csv.field_size_limit(sys.maxsize)
        # get args as list using csv reader
        args = list(csv.reader(line))
        doc_id = args[0]
        doc_title = args[1]
        doc_text = args[2]

        # Cleaning
        text = doc_title + " " + doc_text # combine title and body
        text = re.sub(r"[^a-zA-Z0-9 ]+", "", text) # remove non-alphanumerics
        text = text.casefold() # convert upper to lower case
        words = text.split() # split into whitespace-delimited
        # remove stop words
        with open("stopwords.txt",'r') as stop_file:
            stop_words = dict(stop_file.readLines())
            for word in words:
                if word in stop_words:
                    words.remove(word)
        # print all the words in form doc_id _ word \t 1
        for word in words:
            print(f"{doc_id}_{word}\t1")
