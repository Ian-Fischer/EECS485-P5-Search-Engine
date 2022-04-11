"""Index Server."""
import flask
import math
from flask import g
import re
import index
import pathlib
from collections import Counter

# All necessary globals for the app


def clean_query(query):
    """Clean given query."""
    query = re.sub(r"[^a-zA-Z0-9 ]+", "", query) # remove non-alphanumerics
    query = query.casefold() # convert upper to lower case
    query = query.split() # split into whitespace-delimited
    # remove stop words
    query = [word for word in query if word+'\n' not in g.stop_words]
    return query

def read_stopwords(index_dir):
    """Read stopwords into memory."""
    path = index_dir / "stopwords.txt"
    with open(path, "r", encoding="utf-8") as file:
        g.stop_words = list(file.readlines())


def read_pagerank(index_dir):
    """Read pagerank into memory."""
    path = index_dir / "pagerank.out"
    # initialize the pagerank dict, {doc_id: pagerank score}
    g.pagerank = {}
    with open(path, "r", encoding="utf-8") as file:
        for line in file:
            line = line.split(",")
            g.pagerank[line[0]] = int(line[1])
        

def read_inverted_index(index_dir):
    """
    Read inverted index into memory.
    inverted_index = {
        word: {
            doc_id: {
                idf_k
                norm_factor d_i
            }
            ...
        }
        ...
    }
    """
    g.inverted_index = {}
    # get the path that we set when starting server
    path = index_dir / "inverted_index" / index.app.config["INDEX_PATH"]
    with open(path, "r", encoding="utf-8") as file:
        # go over the whole file
        for line in file:
            # split over white space
            line = line.split()
            # word, idf are the first two things in the line
            word = line[0]
            idf_k = float(line[1])
            # for loop, go from index 2 to end, inc. by 3
            dictionaries = {}
            for i in range(2, len(line), 3):
                # get all the variables
                doc_id = float(line[i])
                tf_ik = float(line[i + 1])
                norm_factor = float(line[i + 2])
                # make a dictionary for this document
                dictionaries[doc_id] = {
                    "tf_ik": tf_ik,
                    "norm_factor": norm_factor
                }
            # append all the info for that word into the dictionary
            g.inverted_index[word] = {
                "idf_k": idf_k,
                "docs": dictionaries
            }

@index.app.before_first_request
def startup():
    """Load inverted index, pagerank, and stopwords into memory."""
    index_dir = pathlib.Path(__file__).parent.parent
    read_stopwords(index_dir)
    read_pagerank(index_dir)
    read_inverted_index(index_dir)


@index.app.route("/api/v1/", methods=["GET"])
def services():
    """Return all services of API."""
    services_dir = {
        "hits": "/api/v1/hits/",
        "url": "/api/v1/"
    }
    return flask.jsonify(**services_dir), 200


@index.app.route("/api/v1/hits/", methods=["GET"])
def hits():
    """Return hits from the provided query."""
    # get query and PageRank weight, pr_weight default is .5
    query = flask.request.args("q")
    pr_weight = flask.request.args("w", default=0.5)
    # clean the query
    query = clean_query(query)
    # get all documents that contain all the words in the query
    all_docs = []
    # get all the docs that each word appears in
    for word in query:
        all_docs.append(set(g.inverted_index[word].keys()))
    # if there are none, return an empty query
    if len(all_docs) == 0:
        return "EMPTY QUERY FIX ME " # FIXME FIXME
    docs = all_docs[0]
    # go thorugh all matching documents for each word, and intersect
    # stores only docs that contain every word
    for doc in all_docs:
        docs = docs.intersection(doc)
    # now, we have all docs that all words appear in
    # next, calc score for each doc
    count = Counter(query)
    results = []
    for doc in docs:
        # build q: <term freq in query>*<idf_k>
        q_vect = []
        # build d_i: <term freq in doc>*<idf>
        d_vect = []
        for word in query:
            q_vect.append(count[word]*g.inverted_index[word]["idf_k"])
            d_vect.append(g.inverted_index[word][doc]["tf_ik"]*g.inverted_index[word]["idf_k"])
        q_dot_d = sum(i[0] * i[1] for i in zip(q_vect, d_vect))
        norm_q = math.sqrt(sum(q**2 for q in q_vect))


    

