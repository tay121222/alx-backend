#!/usr/bin/env python3
"""
Deletion-resilient hypermedia pagination
"""

import csv
import math
from typing import List, Dict


class Server:
    """Server class to paginate a database of popular baby names.
    """
    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        self.__dataset = None
        self.__indexed_dataset = None

    def dataset(self) -> List[List]:
        """Cached dataset
        """
        if self.__dataset is None:
            with open(self.DATA_FILE) as f:
                reader = csv.reader(f)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]

        return self.__dataset

    def indexed_dataset(self) -> Dict[int, List]:
        """Dataset indexed by sorting position, starting at 0
        """
        if self.__indexed_dataset is None:
            dataset = self.dataset()
            truncated_dataset = dataset[:1000]
            self.__indexed_dataset = {
                i: dataset[i] for i in range(len(dataset))
            }
        return self.__indexed_dataset

    def get_hyper_index(self, index: int = None, page_size: int = 10) -> Dict:
        """method returns a dictionary with the following
        - the current start index of the return page
        - the next index to query with
        - the current page size
        - the actual page of the dataset"""
        indexed_dataset = self.indexed_dataset()
        total = len(indexed_dataset)

        if index is None:
            index = 0
        assert index is None or (0 <= index < total)

        temp = []
        next_index = index

        while next_index < total and len(temp) < page_size:
            if next_index in indexed_dataset:
                temp.append(next_index)
            next_index += 1

        data = [indexed_dataset[v] for v in temp]
        next_index = temp[-1] + 1 if temp else None

        hyper_response = {
            'index': index,
            'data': data,
            'page_size': len(data),
            'next_index': next_index if next_index < total else None
        }
        return hyper_response
