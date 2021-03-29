
from flask import Flask
from datetime import datetime
from block_core.blocked import blocked_to_json
from block_server.data_cache import DataCache
from block_server.collector import collect
import threading


def create_app(cache):

    app = Flask(__name__)


    @app.route('/')
    def get():
        current = cache.get_all_since(datetime(2020, 1, 1, 0, 0, 0))

        items = [blocked_to_json(blocked) for blocked in current]
        return items

    return app


def go():
    cache = DataCache()
    app = create_app(cache)
    t = threading.Thread(target=collect(), args=(cache))
    t.start()
    app.run(host='0.0.0.0', port=5000)


if __name__ == '__main__':
    go()