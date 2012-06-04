#!/usr/bin/env python
# -*- coding: utf-8 -*-

class Integer:
    def __init__(self):
        self.constants = {"null": 0, "eins": 1, "zwei": 2, "zehn": 10}
        self.functions = {"add": self.add, "sub": self.sub}
        self.predicates = {"eq": self.eq, "lt": self.lt}

    def getConstant(self, token):
        return self.constants[token]

    def processFunction(self, token, params):
        return self.functions[token](params)

    def processPredicate(self, token, params):
        return self.predicates[token](params)

    def add(self, params):
        assert(len(params) == 2)
        return params[0] + params[1]

    def sub(self, params):
        assert(len(params) == 2)
        return params[0] - params[1]

    def eq(self, params):
        assert(len(params) == 2)
        return params[0] == params[1]

    def lt(self, params):
        assert(len(params) == 2)
        return params[0] < params[1]
