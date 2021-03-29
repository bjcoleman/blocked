
from datetime import timedelta
from block_core.blocked import Blocked


class DataCache:
    """
    This class represents a time-limited cache of blocked traffic data.
    By default, it stores the last 10 seconds of data.  This cache is
    approximate, in that each time new data is added, all data older
    than 10 seconds is removed.

    When data is added, if the timestamp equals the previous timestamp,
    1 ms is added to ensure monotone increasing values.

    Users can obtain all data since a stated timestamp, which will
    return all available data strictly *after* the given timestamp.
    """

    def __init__(self, cache_length_in_seconds=10):
        self.cache = []
        self.cache_length_in_seconds = cache_length_in_seconds

    def get_all_since(self, timestamp):
        """
        Gets all blocked instances where the timestamp is strictly
        greater than the timestamp parameter

        :param timestamp: timestamp of the last data recieved (to ms accuracy)
        :return: all blocked instances with timestamp strictly greater than
           the timestamp parameter
        """
        return [item for item in self.cache if item.timestamp > timestamp]

    def add(self, blocked):
        """
        Add the instance to the cache
        :param blocked:
        :return: None
        """
        if len(self.cache) > 0 and blocked.timestamp <= self.cache[-1].timestamp:
            blocked = Blocked(self.cache[-1].timestamp + timedelta(microseconds=1),
                              blocked.ip, blocked.protocol)

        self.cache.append(blocked)

        cutoff = blocked.timestamp - timedelta(seconds=self.cache_length_in_seconds)
        while self.cache[0].timestamp <= cutoff:
            del self.cache[0]