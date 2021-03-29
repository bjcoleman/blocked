
from pytest import fixture

from block_server.data_cache import DataCache
from block_core.blocked import Blocked

from datetime import datetime


@fixture()
def cache():
    return DataCache()


def test_new_instance_has_no_data(cache):
    assert cache.get_all_since(0) == []


def blocked_at(timestamp):
    return Blocked(timestamp, '1.1.1.1', 'tcp')


def test_values_remembered(cache):
    # add 1 second after midnight
    timestamp = datetime(2020, 1, 1, 0, 0, 1, 0)
    blocked = blocked_at(timestamp)
    cache.add(blocked)
    assert cache.get_all_since(datetime(2020, 1, 1, 0, 0, 0, 0)) == [blocked]


def test_data_dropped_after_10_seconds(cache):
    timestamp = datetime(2020, 1, 1, 0, 0, 1, 0)
    blocked = blocked_at(timestamp)
    cache.add(blocked)

    timestamp_plus_20 = datetime(2020, 1, 1, 0, 0, 21, 0)
    blocked2 = blocked_at(timestamp_plus_20)
    cache.add(blocked2)

    timestamp_early = datetime(2020, 1, 1, 0, 0, 0, 0)
    assert cache.get_all_since(timestamp_early) == [blocked2]


def test_data_is_stored_monotone_increasing(cache):
    timestamp1 = datetime(2020, 1, 1, 0, 0, 1, 0)
    blocked1 = blocked_at(timestamp1)
    cache.add(blocked1)

    timestamp2 = datetime(2020, 1, 1, 0, 0, 1, 0)
    blocked2 = blocked_at(timestamp2)
    cache.add(blocked2)

    timestamp3 = datetime(2020, 1, 1, 0, 0, 1, 0)
    blocked3 = blocked_at(timestamp3)
    cache.add(blocked3)

    expected_timestamp2 = datetime(2020, 1, 1, 0, 0, 1, 1)
    expected_blocked2 = blocked_at(expected_timestamp2)

    expected_timestamp3 = datetime(2020, 1, 1, 0, 0, 1, 2)
    expected_blocked3 = blocked_at(expected_timestamp3)

    timestamp_early = datetime(2020, 1, 1, 0, 0, 0, 0)
    assert cache.get_all_since(timestamp_early) == [blocked1, expected_blocked2, expected_blocked3]


def test_get_all_since_with_last_timestamp_is_empty(cache):
    timestamp1 = datetime(2020, 1, 1, 0, 0, 1, 0)
    blocked1 = blocked_at(timestamp1)
    cache.add(blocked1)

    assert cache.get_all_since(timestamp1) == []


def test_get_all_since_gives_back_partial_data(cache):

    for ms in range(10):
        timestamp = datetime(2020, 1, 1, 0, 0, 1, ms)
        blocked = blocked_at(timestamp)
        cache.add(blocked)

    assert len(cache.get_all_since(datetime(2020, 1, 1, 0, 0, 1, 5))) == 4


def test_get_data_only_gives_within_cache_length(cache):

    for seconds in range(20):
        timestamp = datetime(2020, 1, 1, 0, 0, seconds)
        blocked = blocked_at(timestamp)
        cache.add(blocked)

    assert len(cache.get_all_since(datetime(2020, 1, 1, 0, 0, 0))) == 10
