import sys
import itertools
from inverted_index.reduce0 import reduce_one_group, keyfunc

if __name__ == "__main__":
    # reduce each group given to us to count how many docid_word
    for key, group in itertools.groupby(sys.stdin, keyfunc):
        reduce_one_group(key, group)
