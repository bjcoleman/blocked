
from block_server.server import create_app
from block_server.data_cache import DataCache
from block_core.blocked import Blocked
import datetime


def test_no_timestamp():
    app = create_app(None)
    app.testing = True
    client = app.test_client()

    result = client.get('/')
    assert result.status_code == 400


def test_no_data():
    app = create_app(DataCache())
    app.testing = True
    client = app.test_client()

    params = {'timestamp': 0}
    result = client.get(data=params)

    assert result.status_code == 200
    assert result.get_json() == []


def test_all_data():
    cache = DataCache()
    cache.add(Blocked(datetime.datetime(2021, 1, 2, 0, 15, 30), '1.1.1.1', 'tcp'))
    cache.add(Blocked(datetime.datetime(2021, 1, 2, 0, 15, 31), '1.1.1.1', 'tcp'))

    app = create_app(cache)
    app.testing = True
    client = app.test_client()

    params = {'timestamp': 0}
    result = client.get(data=params)

    assert result.status_code == 200
    assert len(result.get_json()) == 2


def test_subset_of_data():
    cache = DataCache()
    cache.add(Blocked(datetime.datetime(2021, 1, 2, 0, 15, 35), '1.1.1.1', 'tcp'))
    cache.add(Blocked(datetime.datetime(2021, 1, 2, 0, 15, 40), '1.1.1.1', 'tcp'))

    app = create_app(cache)
    app.testing = True
    client = app.test_client()

    params = {'timestamp': datetime.datetime(2021, 1, 2, 0, 15, 36).timestamp()}
    result = client.get(data=params)

    assert result.status_code == 200
    assert len(result.get_json()) == 1


def test_bad_timestamp():
    app = create_app(None)
    app.testing = True
    client = app.test_client()

    params = {'timestamp': 'hello'}
    result = client.get(data=params)

    assert result.status_code == 400
