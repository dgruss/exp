#!/usr/bin/env python
# -*- coding: utf-8 -*-

class Integer:
    def __init__(self):
        self.constants = {"null": 0, "eins": 1, "zwei": 2, "zehn": 10}
        self.functions = {"add": self.add, "sub": self.sub}
        self.predicates = {"eq": self.eq, "lt": self.lt}

    def add(self, param1, param2):
        return param1 + param2

    def sub(self, param1, param2):
        return param1 - param2

    def eq(self, param1, param2):
        return param1 == param2

    def lt(self, param1, param2):
        return param1 < param2
