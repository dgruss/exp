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

def parse(program):
    result = []
    for line in program:
        try:
                tokens = exp.parseString(line)
                result.append(tokens[0])
        except ParseException, err:
                print " "*err.loc + "^\n" + err.msg
                print err
    call = result.pop()
    return (call, parseDelta(result))


exp = Forward()

name = Regex("\w+")
paramsDef = Group(Suppress("(") + name + ZeroOrMore(Suppress(",") + name) + Suppress(")"))
params = Group(Suppress("(") + exp + ZeroOrMore(Suppress(",") + exp) + Suppress(")"))
function = name + params
conditional = "if" + name + Suppress("?") + params + Suppress("then") + exp + Suppress("else") + exp
definition = name + paramsDef + Suppress("=") + exp

exp << Group(conditional | definition | function | name)

(call, delta) = parse(["E(x,y,z) = if eq?(x,y,z) then null else add(x,y,z)", "E(0)"])
