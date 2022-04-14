"""Search development configuration."""
import pathlib

SEARCH_INDEX_SEGMENT_API_URLS = [
    "http://localhost:9000/api/v1/hits/",
    "http://localhost:9001/api/v1/hits/",
    "http://localhost:9002/api/v1/hits/",
]

# Root of this application, useful if it doesn't occupy an entire domain
APPLICATION_ROOT = '/'

SEARCH_ROOT = pathlib.Path(__file__).resolve().parent.parent

# Database file is var/index.sqlite3
DATABASE_FILENAME = SEARCH_ROOT.parent/'var'/'index.sqlite3'
