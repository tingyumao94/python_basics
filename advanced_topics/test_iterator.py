#!/usr/bin/python
class Iter:
    def __init__(self, max_limit):
        self.cnt = 0
        self.max_limit = max_limit

    def __next__(self):
