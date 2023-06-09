#!/usr/bin/env python3
"""MapReduce stage 1 reduce."""
import sys
import itertools
from reduce0 import reduce_one_group, keyfunc

if __name__ == "__main__":
    # reduce each group given to us to count how many docid_word
    for key, group in itertools.groupby(sys.stdin, keyfunc):
        reduce_one_group(key, group)
