#!/usr/bin/python3
"""class LFUCache"""
from base_caching import BaseCaching


class LFUCache(BaseCaching):
    """Class that inherits from BaseCaching and is a caching system"""

    def __init__(self):
        """Initialization"""
        self.used_key = {}
        self.times_key = {}
        self.time = 0
        super().__init__()

    def put(self, key, item):
        """Put item in cache"""

        if key is None or item is None:
            return

        if key is not None and item is not None:
            if len(
                    self.cache_data
                    ) >= self.MAX_ITEMS and key not in self.cache_data:
                min_used_count = min(self.used_key.values())
                least_frequent_keys = [
                        k for k, v in self.used_key.items()
                        if v == min_used_count
                        ]
                least_recently_used = min(
                        least_frequent_keys, key=lambda k: self.times_key[k]
                        )
                self.cache_data.pop(least_recently_used)
                del self.used_key[least_recently_used]
                del self.times_key[least_recently_used]
                print('DISCARD:', least_recently_used)

        self.cache_data[key] = item
        self.used_key[key] = self.used_key.get(key, 0) + 1
        self.times_key[key] = self.time
        self.time += 1

    def get(self, key):
        """Get item from cache"""
        if key is None or key not in self.cache_data:
            return None

        self.used_key[key] = self.used_key.get(key, 0) + 1
        self.times_key[key] = self.time
        self.time += 1

        return self.cache_data[key]
