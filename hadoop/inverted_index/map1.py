#!/usr/bin/env python3
"""Map 1."""
import sys
import re
import csv

if __name__ == "__main__":
    # set csv max size
    csv.field_size_limit(sys.maxsize)
    for line in csv.reader(sys.stdin):
        doc_id = line[0]
        doc_title = line[1]
        doc_text = line[2]
        # Cleaning
        text = doc_title + " " + doc_text
        text = re.sub(r"[^a-zA-Z0-9 ]+", "", text)
        text = text.casefold()
        words = text.split()
        # remove stop words
        with open("stopwords.txt", 'r') as stop_file:
            stop_words = list(stop_file.readlines())
            words = [word for word in words if word+'\n' not in stop_words]
        # print all the words in form doc_id _ word \t 1
        for word in words:
            print(f"{doc_id}_{word}\t1")
