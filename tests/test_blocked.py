
from block_core.blocked import Blocked, blocked_to_json, json_to_blocked
import datetime


def test_blocked_to_json():
    blocked = Blocked(datetime.datetime(2021, 1, 2, 0, 15, 30), '1.1.1.1', 'tcp')
    assert blocked_to_json(blocked) == '{"timestamp": "2021/01/02 00:15:30", "ip": "1.1.1.1", "protocol": "tcp"}'


def test_json_to_blocked():
    blocked = json_to_blocked('{"timestamp": "2021/01/02 00:15:30", "ip": "1.1.1.1", "protocol": "tcp"}')
    expected = Blocked(datetime.datetime(2021, 1, 2, 0, 15, 30), '1.1.1.1', 'tcp')
    assert blocked == expected


def test_loop_from_string():
    start = '{"timestamp": "2021/01/02 00:15:30", "ip": "1.1.1.1", "protocol": "tcp"}'
    assert blocked_to_json(json_to_blocked(start)) == start


def test_loop_from_blocked():
    start = Blocked(datetime.datetime(2021, 1, 2, 0, 15, 30), '1.1.1.1', 'tcp')
    assert json_to_blocked(blocked_to_json(start)) == start
