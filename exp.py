#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from parse import parse_exp
from integer import Integer

def formatExp(psi, delta, omega, exp):
    """ Function for formatted output of an expression """

    if (exp[0] in psi.constants) or (exp[0] in omega):
        # constant
        # variable
        return exp[0]

    if (exp[0] in psi.functions) or (exp[0] in delta):
        # function(param1,param2,...)
        # E(x)
        return exp[0] + "(" + ", ".join([formatExp(psi, delta, omega, p) for p in exp[1]]) + ")"

    if exp[0] in psi.predicates:
        # predicate?(param1,param2,...)
        return exp[0] + "?(" + ", ".join([formatExp(psi, delta, omega, p) for p in exp[1]]) + ")"

    if exp[0] == "if":
        # if predicate?(param1,param2,...) then token1 else token2
        terms = {"predicate": exp[1],
                 "parameters": ",".join([formatExp(psi, delta, omega, p) for p in exp[2]]),
                 "token1": formatExp(psi, delta, omega, exp[3]),
                 "token2": formatExp(psi, delta, omega, exp[4])}
        return "if %(predicate)s?(%(parameters)s) then %(token1)s else %(token2)s" % terms

    return exp[0]

def I(indent, psi, delta, omega, n, exp):
    """ The Interpretion Function """

    # CONSTANT
    if exp[0] in psi.constants:
        result = psi.constants[exp[0]]
        print "%s= %s" % (" " * indent, result)
        return result

    # VARIABLE
    if exp[0] in omega:
        result = omega[exp[0]]
        print "%s= omega%d(%s)" % (" " * indent, n, exp[0])
        print "%s= %s" % (" " * indent, result)
        return result

    # DATATYPE FUNCTION
    if exp[0] in psi.functions:
        print "%s= %s(%s)" % (" " * indent, exp[0], ", ".join(["I(delta, omega%d, %s)" % (n, p[0]) for p in exp[1]]))
        params = []
        for param in exp[1]:
            print "%s  I(delta, omega%d, %s)" % (" " * indent, n, formatExp(psi, delta, omega, param))
            params.append(I(indent + 2, psi, delta, omega, n, param))
        result = psi.functions[exp[0]](*params)
        print "%s= %s" % (" " * indent, result)
        return result

    # CONDITIONAL
    if exp[0] == "if":
        assert exp[1] in psi.predicates

        print "%s  Nebenrechnung:" % (" " * indent)
        print "%s    I(delta, omega%d, %s)" % (" " * indent, n, formatExp(psi, delta, omega, exp[1:3]))
        print "%s    = %s?(%s)" % (" " * indent, exp[1], ", ".join(["I(delta, omega%d, %s)" % (n, p[0]) for p in exp[2]]))

        params = []
        for param in exp[2]:
            print "%s      I(delta, omega%d, %s)" % (" " * indent, n, formatExp(psi, delta, omega, param))
            params.append(I(indent + 6, psi, delta, omega, n, param))

        print "%s    = %s?(%s)" % (" " * indent, exp[1], ",".join(map(str, params)))
        if psi.predicates[exp[1]](*params):
            print "%s    = T" % (" " * indent)
            print "%s= I(delta, omega%d, %s)" % (" " * indent, n, formatExp(psi, delta, omega, exp[3]))
            return I(indent, psi, delta, omega, n, exp[3])
        else:
            print "%s    = F" % (" " * indent)
            print "%s= I(delta, omega%d, %s)" % (" " * indent, n, formatExp(psi, delta, omega, exp[4]))
            return I(indent, psi, delta, omega, n, exp[4])

    # FUNCTION
    if exp[0] in delta:
        # fill new omega environment
        print "%s  Neues Environment (omega%d):" % (" " * indent, n + 1)
        new_omega = dict()
        paramNames = delta[exp[0]][0]
        paramList = exp[1]
        for i in range(0, len(paramNames)):
            print "%s    omega%u(%s)" % (" " * indent, n + 1, paramNames[i])
            print "%s    = I(delta, omega%u, %s)" % (" " * indent, n, formatExp(psi, delta, omega, paramList[i]))
            new_omega[paramNames[i]] = I(indent + 4, psi, delta, omega, n, paramList[i])
        # call I with implementation of the function and new omega environment
        implementation = delta[exp[0]][1]
        print "%s= I(delta,omega%u,%s)" % (" " * indent, n + 1, formatExp(psi, delta, omega, implementation))
        return I(indent, psi, delta, new_omega, n + 1, implementation)

    print "Fatal error parsing: ", exp
    exit(-1)

if __name__ == "__main__":
    programm = []
    if sys.argv[1:]:
        with open(sys.argv[1]) as inputfile:
            programm = inputfile.readlines()
    else:
        programm = ["E(x) = if eq?(x,null) then null else add(x,E(sub(x,eins)))", "E(zwei)"]

    exp, delta = parse_exp(programm)
    psi = Integer()
    omega = dict()

    print "I(delta,omega0,%s)" % formatExp(psi, delta, omega, exp)
    print "Result: %s" % I(0, psi, delta, omega, 0, exp)
