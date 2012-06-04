#!/usr/bin/env python
# -*- coding: utf-8 -*-

class Integer:
    def __init__(self):
        self = self

    def hasConstant(self, token):
        return self.constants.has_key(token)

    def getConstant(self, token):
        return self.constants[token]

    def hasFunction(self, token):
        return self.functions.has_key(token)

    def processFunction(self, token, params):
        return self.functions[token](self, params)

    def hasPredicate(self, token):
        return self.predicates.has_key(token)

    def processPredicate(self, token, params):
        return self.predicates[token](self, params)

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

    constants = {"null": 0, "eins": 1, "zwei": 2, "zehn": 10}
    functions = {"add": add, "sub": sub}
    predicates = {"eq": eq, "lt": lt}
