#!/usr/bin/python3
"""class LRUCache"""
from base_caching import BaseCaching


class LRUCache(BaseCaching):
    """inherits from BaseCaching and is a caching system"""

    def __init__(self):
        """Initialization"""
        super().__init__()
        self.templist = []

    def put(self, key, item):
        """Add item to cache"""
        if key is None or item is None:
            return

        if key in self.cache_data:
            self.templist.remove(key)
        elif len(self.cache_data) >= self.MAX_ITEMS:
            discard_key = self.templist.pop(0)
            del self.cache_data[discard_key]
            print("DISCARD:", discard_key)

        self.cache_data[key] = item
        self.templist.append(key)

    def get(self, key):
        """Get item from cache"""
        if key is None or key not in self.cache_data:
            return None
        self.templist.remove(key)
        self.templist.append(key)

        return self.cache_data[key]
