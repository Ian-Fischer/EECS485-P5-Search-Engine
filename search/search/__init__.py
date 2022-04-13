"""Initialize search application."""
import flask
import os

app = flask.Flask(__name__, template_folder="templates")
app.config.from_object('search.config')
# naughty flask
import search.views  # noqa: E402  pylint: disable=wrong-import-position
import search.model  # noqa: E402  pylint: disable=wrong-import-position
