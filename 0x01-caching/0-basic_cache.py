#!/usr/bin/python3
"""class BasicCache"""
from importlib import import_module
BaseCaching = import_module("base_caching").BaseCaching


class BasicCache(BaseCaching):
    """class BasicCache that inherits from BaseCaching"""

    def put(self, key, item):
        """Put item to cache"""
        if key is None or item is None:
            return
        self.cache_data[key] = item

    def get(self, key):
        """Get item from cache"""
        if key is None or key not in self.cache_data:
            return None
        return self.cache_data[key]
