"""Map 1."""
import sys
import re

for line in sys.stdin:
    args = line.split(",")
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
        stop_words = stop_file.readLines()
        for word in stop_words:
            words.remove(word)
    # print all the words
    for word in words:
