
from flask import Flask, jsonify, request
from datetime import datetime
from block_core.blocked import blocked_to_dict
from block_server.data_cache import DataCache
from block_server.collector import Collector


def create_app(cache):

    app = Flask(__name__)

    @app.route('/')
    def get():
        timestamp_str = request.args.get('timestamp')
        if timestamp_str is None:
            return "['error': 'provide timestemp']", 400

        try:
            timestamp = datetime.fromtimestamp(float(timestamp_str))
        except ValueError:
            return "['error': 'timestamp must be a float']", 400

        current = cache.get_all_since(timestamp)

        items = [blocked_to_dict(blocked) for blocked in current]
        return jsonify(items)

    return app


def go():
    cache = DataCache()
    app = create_app(cache)
    collector = Collector(cache)
    collector.start()
    app.run(host='0.0.0.0', port=5000)


if __name__ == '__main__':
    go()