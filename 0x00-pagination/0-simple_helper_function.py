#!/usr/bin/env python3
"""function named index_range"""
from typing import Tuple


def index_range(page: int, page_size: int) -> Tuple[int, int]:
    """takes two integer arguments page and page_size"""
    start = (page - 1) * page_size
    end = start + page_size
    return start, end
