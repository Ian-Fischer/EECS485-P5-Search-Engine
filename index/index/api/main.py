"""Index Server."""
import math
import re
import pathlib
from collections import Counter
import flask
import index

stop_words = []
pagerank = {}
inverted_index = {}


def get_tfidf(q_vect, d_vect, tmp, doc):
    """Get tfidf for given vectors."""
    q_dot_d = sum(i[0] * i[1] for i in zip(q_vect, d_vect))
    norm_q = math.sqrt(sum(q**2 for q in q_vect))
    norm_d = math.sqrt(inverted_index[tmp]["docs"][doc]["norm_factor"])
    return q_dot_d / (norm_q * norm_d)


def clean_query(query):
    """Clean given query."""
    query = re.sub(r"[^a-zA-Z0-9 ]+", "", query)
    query = query.casefold()
    query = query.split()
    # remove stop words
    query = [word for word in query if word not in stop_words]
    return query


def read_stopwords(index_dir):
    """Read stopwords into memory."""
    path = index_dir / "stopwords.txt"
    with open(path, "r", encoding="utf-8") as file:
        for stopword in list(file.readlines()):
            stop_words.append(stopword.replace("\n", ""))


def read_pagerank(index_dir):
    """Read pagerank into memory."""
    path = index_dir / "pagerank.out"
    # initialize the pagerank dict, {doc_id: pagerank score}
    with open(path, "r", encoding="utf-8") as file:
        for line in file:
            line = line.replace("\n", "")
            line = line.split(",")
            pagerank[line[0]] = float(line[1])


def read_inverted_index(index_dir):
    """Read inverted index into memory."""
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
                doc_id = line[i]
                tf_ik = float(line[i + 1])
                norm_factor = float(line[i + 2])
                # make a dictionary for this document
                dictionaries[doc_id] = {
                    "tf_ik": tf_ik,
                    "norm_factor": norm_factor
                }
            # append all the info for that word into the dictionary
            inverted_index[word] = {
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
def search_results():
    """Return hits from the provided query."""
    # get query and PageRank weight, pr_weight default is .5
    query = flask.request.args.get("q")
    pr_weight = float(flask.request.args.get("w", default=0.5))
    # clean the query
    query = clean_query(query)
    # get all documents that contain all the words in the query
    all_docs = []
    # get all the docs that each word appears in
    for word in query:
        if word in inverted_index:
            keys = inverted_index[word]["docs"].keys()
            all_docs.append(set(keys))
        # if a word is not in our index, return empty
        else:
            return flask.jsonify(**{"hits": []}), 200
    docs = all_docs[0]
    # go thorugh all matching documents for each word, and intersect
    # stores only docs that contain every word
    for doc in all_docs:
        docs = docs.intersection(doc)
    # now, we have all docs that all words appear in
    # next, calc score for each doc
    hits = []
    for doc in docs:
        # build q: <term freq in query>*<idf_k>
        q_vect = []
        # build d_i: <term freq in doc>*<idf>
        d_vect = []
        tmp = ""
        for word in query:
            tmp = word
            q_vect.append(Counter(query)[word]*inverted_index[word]["idf_k"])
            john = inverted_index[word]["docs"][doc]["tf_ik"]
            kyle = inverted_index[word]["idf_k"]
            d_vect.append(john*kyle)
            tfidf = get_tfidf(q_vect, d_vect, tmp, doc)
        hits.append({
            "docid": int(doc),
            "score": pr_weight*pagerank[doc] + (1 - pr_weight)*tfidf
        })
    # sort the results by score and return
    output = {
        "hits": sorted(hits, key=lambda x: x["score"], reverse=True)
    }
    return flask.jsonify(**output), 200
