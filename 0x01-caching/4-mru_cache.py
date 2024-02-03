#!/usr/bin/python3
"""class MRUCache"""
from base_caching import BaseCaching


class MRUCache(BaseCaching):
    """inherits from BaseCaching and is a caching system"""

    def __init__(self):
        """Initialization"""
        super().__init__()
        self.item_key = None

    def put(self, key, item):
        """Add item to cache"""
        if key is None or item is None:
            return

        if key in self.cache_data:
            self.cache_data[key] = item
            self.item_key = key
            return

        if len(self.cache_data) >= self.MAX_ITEMS:
            discarded_key = self.item_key
            print("DISCARD:", discarded_key)
            del self.cache_data[discarded_key]

        self.cache_data[key] = item
        self.item_key = key

    def get(self, key):
        """Get item from cache"""
        if key is None or key not in self.cache_data:
            return None

        self.item_key = key
        return self.cache_data[key]
