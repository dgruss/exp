#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pyparsing import ParseException, Forward, ZeroOrMore, Regex, Group, Suppress

def parseDelta(program):
    delta = dict()
    for line in program:
        name = line[0]
        params = line[1]
        implementation = line[2]
        delta[name] = (params, implementation)
    return delta

def createEXPParser():
    exp = Forward()
    name = Regex("\w+")
    paramsDef = Group(Suppress("(") + name + ZeroOrMore(Suppress(",") + name) + Suppress(")"))
    params = Group(Suppress("(") + exp + ZeroOrMore(Suppress(",") + exp) + Suppress(")"))
    conditional = "if" + name + Suppress("?") + params + Suppress("then") + exp + Suppress("else") + exp
    definition = name + paramsDef + Suppress("=") + exp
    function = name + params
    exp << Group(conditional | definition | function | name)
    return exp

def parse_exp(program):
    """ Function for parsing a programm written in EXP """
    exp = createEXPParser()
    
    result = []
    for line in program:
        try:
            tokens = exp.parseString(line)
            result.append(tokens[0])
        except ParseException, err:
            print " "*err.loc + "^\n" + err.msg
            print err
    return (result.pop(), parseDelta(result))

if __name__ == "__main__":
    (call, delta) = parse_exp(["E(x,y,z) = if eq?(x,y,z) then null else add(x,y,z)", "E(0)"])
