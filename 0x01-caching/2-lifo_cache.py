#!/usr/bin/python3
"""class LIFOCache"""
from base_caching import BaseCaching


class LIFOCache(BaseCaching):
    """class LIFOCache that inherits from BaseCaching
    and is a caching system"""

    def __init__(self):
        """Initialization"""
        super().__init__()

    def put(self, key, item):
        """Put item into cache"""
        if key is None or item is None:
            return

        if len(self.cache_data) >= self.MAX_ITEM:
            last_item = next(reversed(self.cache_data))
            print("DISCARD:", last_item)
            del self.cache_data[last_item]

        self.cache_data[key] = item

    def get(self, key):
        """Get item from cache"""
        if key is None or key not in self.cache_data:
            return None
        return self.cache_data[key]
