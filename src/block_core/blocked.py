from collections import namedtuple
import json
import datetime


Blocked = namedtuple('Blocked', ['timestamp', 'ip', 'protocol'])


def blocked_to_json(blocked):
    timestamp = blocked.timestamp.strftime('%Y/%m/%d %H:%M:%S')
    ret = {'timestamp': timestamp,
           'ip': blocked.ip,
           'protocol': blocked.protocol}
    return json.dumps(ret)


def json_to_blocked(json_str):
    param = json.loads(json_str)
    return Blocked(datetime.datetime.strptime(param['timestamp'], '%Y/%m/%d %H:%M:%S'),
                   param['ip'],
                   param['protocol'])