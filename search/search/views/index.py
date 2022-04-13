"""Server-side dynamic pages."""
import search
import flask
import sqlite3
import requests
import threading
import heapq

def index_server_req(url, results, index):
    """Make request to index server."""
    # make a request to the server using url
    # TODO: exception handling??
    r = requests.get(url)
    # put the results into the correct index
    dictionaries = r.json()["hits"]
    results[index] = [(x["score"], x["docid"]) for x in dictionaries]

    
@search.app.route("/", methods=["GET"])
def show_index():
    """Renders the home page."""
    # build context w/ no search & weight & results
    context = {
        "query": "",
        "weight": "0.5",
    }
    return flask.render_template("index.html", **context)

@search.app.route("/", methods=['GET'])
def sling():
    """Sling there like slingwear."""
    # Get the query & weight
    query = flask.request.args.get('q')
    weight = flask.request.args.get('w')
    # Build the url
    base = search.app.config["SEARCH_INDEX_SEGMENT_API_URLS"]
    url0 = base[0]+f"?q={query}&w={weight}"
    url1 = base[1]+f"?q={query}&w={weight}"
    url2 = base[2]+f"?q={query}&w={weight}"
    # List to store the results in
    results = [None, None, None]
    # Call the index server to get page rankings
    thread0 = threading.Thread(target=index_server_req, args=(url0, results, 0))
    thread0.start()
    thread1 = threading.Thread(target=index_server_req, args=(url1, results, 1))
    thread1.start()
    thread2 = threading.Thread(target=index_server_req, args=(url2, results, 2))
    thread2.start()
    # close all threads after they are made
    thread0.join()
    thread1.join()
    thread2.join()
    # Use heapq.merge() to combine them
    num_results = 0
    ranked_pages = []
    for line in heapq.merge(*results):
        ranked_pages.append(line)
        num_results += 1
        if num_results == 10:
            break
    # Connect to database
    connection = search.model.get_db()
    connection.row_factory = sqlite3.Row
    # Build context by going to database & getting info
    # TODO: not in db?
    for i, result in enumerate(ranked_pages):
        document = connection.execute(
            "SELECT title, url, summary "
            "FROM Documents "
            "WHERE docid = ? ",
            (result[1], )
        ).fetchone()
        ranked_pages[i] = {
            "title": document[0],
            "url": document[1],
            "summary": document[2]
        }
    # Build context
    context = {
        "query": query,
        "weight": weight,
        "results": ranked_pages
    }
    # Display to user
    return flask.render_template("results.html", **context)
    

    
