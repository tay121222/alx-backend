#!/usr/bin/python3
"""class LIFOCache"""
from base_caching import BaseCaching


class LIFOCache(BaseCaching):
    """class LIFOCache that inherits from BaseCaching
    and is a caching system"""

    def __init__(self):
        """Initialization"""
        super().__init__()
        self.templist = []

    def put(self, key, item):
        """Put item into cache"""
        if key is not None and item is not None:
            self.cache_data[key] = item

            if len(self.cache_data) > BaseCaching.MAX_ITEMS:
                discarded_key = self.last_key
                print("DISCARD: {}".format(discarded_key))
                del self.cache_data[discarded_key]

            self.last_key = key

    def get(self, key):
        """Get item from cache"""
        if key is None or key not in self.cache_data:
            return None
        return self.cache_data.get(key, None)
