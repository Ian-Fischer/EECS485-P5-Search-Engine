"""Index Server file."""
from email.policy import default
import flask
import index
import pathlib

def read_stopwords(index_dir):
    """Read stopwords into memory."""
    pass


def read_pagerank(index_dir):
    """Read pagerank into memory."""
    pass


def read_inverted_index(index_dir):
    """Read inverted index into memory."""
    pass


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
    

