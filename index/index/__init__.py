# """Insta485 package initializer."""
import flask
import os


# Configure segment, each Index server serves a different segment
app = flask.Flask(__name__)
app.config["INDEX_PATH"] = os.getenv("INDEX_PATH", "inverted_index_1.txt")


# naughty flask
import index.api