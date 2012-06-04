#!/usr/bin/env python
# -*- coding: utf-8 -*-

from parse import parse
from integer import Integer

def formatExp(psi, delta, omega, exp):
    if exp[0] in psi.constants or exp[0] in omega:
        # constant
        return exp[0]
    
    if exp[0] in psi.functions or exp[0] in delta:
        # function(param1,param2,...)
        # E(x)
        return exp[0] + "(" + ",".join([formatExp(psi, delta, omega, p) for p in exp[1]]) + ")"
    
    if exp[0] in psi.predicates:
        # predicate?(param1,param2,...)
        return exp[0] + "?(" + ",".join([formatExp(psi, delta, omega, p) for p in exp[1]]) + ")"
    
    if exp[0] == "if":
        # if predicate?(param1,param2,...) then token1 else token2
        terms = {"predicate": exp[1],
                 "parameters": ",".join([formatExp(psi, delta, omega, p) for p in exp[2]]),
                 "token1": formatExp(psi, delta, omega, exp[3]),
                 "token2": formatExp(psi, delta, omega, exp[4])}
        return "if %(predicate)s?(%(parameters)s) then %(token1)s else %(token2)s" % terms
    
    return exp[0]

def I(indent, psi, delta, (omega, n), exp):
    # CONDITIONAL
    if exp[0] == "if":
        print "%s  Nebenrechnung:" % (" " * indent)
        print "%s    I(δ, ω%d, %s)" % (" " * indent, n, formatExp(psi, delta, omega, exp[1:3]))
        print "%s    = %s?(%s)" % (" " * indent, exp[1], ",".join(["I(δ, ω%d, %s)" % (n, p[0]) for p in exp[2]]))
        if exp[1] in psi.predicates:
            params = []
            for param in exp[2]:
                print "%s      I(δ, ω%u, %s)" % (" " * indent, n, formatExp(psi, delta, omega, param))
                params.append(I(indent + 6, psi, delta, (omega, n), param))
            if psi.processPredicate(exp[1], params):
                print "%s    = %s?(%s)\n%s= T\n%s = I(δ,ω%u,%s)" % (" " * indent, exp[1], `params`[1:-1], " " * (indent + 4), " " * indent, n, formatExp(psi, delta, omega, exp[3]))
                return I(indent, psi, delta, (omega, n), exp[3])
            else:
                print "%s    = %s?(%s)\n%s= F\n%s= I(δ,ω%u,%s)" % (" " * indent, exp[1], `params`[1:-1], " " * (indent + 4), " " * indent, n, formatExp(psi, delta, omega, exp[4]))
                return I(indent, psi, delta, (omega, n), exp[4])
    # CONSTANT
    elif exp[0] in psi.constants:
        result = psi.getConstant(exp[0])
        print "%s= %s" % (" " * indent, result)
        return result
    # VARIABLE
    elif exp[0] in omega: 
        result = omega[exp[0]]
        print "%s= ω%u(%s)\n%s= %s" % (" " * indent, n, exp[0], " " * indent, result)
        return result
    # DATATYPE FUNCTION
    elif exp[0] in psi.functions:
        print "%s= %s(%s)" % (" " * indent, exp[0], ",".join(["I(δ, ω%d, %s)" % (n, p) for p in exp[1]])),
        params = []
        for param in exp[1]:
            print "%sI(δ, ω%u, %s)" % (" " * (indent + 2), n, formatExp(psi, delta, omega, param))
            params.append(I(indent + 2, psi, delta, (omega, n), param))
        result = psi.processFunction(exp[0], params)
        print "%s= %s\n" % (" " * indent, result),
        return result
    # FUNCTION
    elif exp[0] in delta:

        # fill new omega environment
        print "%sNeues Environment (ω%u):" % (" " * (indent + 2), n + 1)
        new_omega = dict()
        paramNames = delta[exp[0]][0]
        paramList = exp[1]
        for i in range(0, len(paramNames)):
            print "%sω%u(%s)\n" % (" " * (indent + 4), n + 1, paramNames[i]),
            print "%s= I(δ, ω%u, %s)" % (" " * (indent + 4), n, formatExp(psi, delta, omega, paramList[i]))
            new_omega[paramNames[i]] = I(indent + 4, psi, delta, (omega, n), paramList[i])
        # call I with implementation of the function and new omega environment
        implementation = delta[exp[0]][1]
        print "%s= I(δ,ω%u,%s)" % (" " * indent, n + 1, formatExp(psi, delta, omega, implementation))
        return I(indent, psi, delta, (new_omega, n + 1), implementation)

    else:
        print "Fatal error parsing: ", exp
        exit(-1)

omega = dict()
psi = Integer()

(exp, delta) = parse(["E(x) = if eq?(x,null) then null else add(x,E(sub(x,eins)))", "E(zwei)"])

print "I(δ,ω0,%s)" % formatExp(psi, delta, omega, exp)
print "Result: %s" % I(0, psi, delta, (omega, 0), exp)
