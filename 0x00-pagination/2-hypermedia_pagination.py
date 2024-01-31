#!/usr/bin/env python3
"""function named index_range"""
import csv
import math
from typing import Tuple, List


def index_range(page: int, page_size: int) -> Tuple[int, int]:
    """takes two integer arguments page and page_size"""
    start = (page - 1) * page_size
    end = start + page_size
    return start, end


class Server:
    """Server class to paginate a database of popular baby names.
    """
    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        self.__dataset = None

    def dataset(self) -> List[List]:
        """Cached dataset
        """
        if self.__dataset is None:
            with open(self.DATA_FILE) as f:
                reader = csv.reader(f)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]

        return self.__dataset

    def get_page(self, page: int = 1, page_size: int = 10) -> List[List]:
        """return the appropriate page of the datase"""
        assert isinstance(page, int) and page > 0
        assert isinstance(page_size, int) and page_size > 0
        dataset = self.dataset()
        start, end = index_range(page, page_size)
        return dataset[start:end]

    def get_hyper(self, page: int = 1, page_size: int = 10) -> dict:
        """ takes the same arguments (and defaults) as get_page
        and returns a dictionary"""
        dataset = self.get_page(page, page_size)
        total = math.ceil(len(self.dataset()) / page_size)
        response = {
            'page_size': len(dataset),
            'page': page,
            'data': dataset,
            'next_page': page + 1 if page < total else None,
            'prev_page': page - 1 if page > 1 else None,
            'total_pages': total
        }
        return response
