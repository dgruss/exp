import sys
def printf(fmt, *varargs):
    sys.stdout.write(fmt % varargs)

from parse import parse
from integer import *

def formatExp(psi, delta, omega, exp):
  if psi.hasConstant(exp[0]) or omega.has_key(exp[0]):
    return exp[0]
  elif psi.hasFunction(exp[0]):
    result = exp[0] + "(" + formatExp(psi, delta, omega, exp[1][0])
    for p in exp[1][1:]:
      result += "," + formatExp(psi, delta, omega, p)
    return result + ")"
  elif psi.hasPredicate(exp[0]):
    result = exp[0] + "?(" + formatExp(psi, delta, omega, exp[1][0])
    for p in exp[1][1:]:
      result += "," + formatExp(psi, delta, omega, p)
    return result + ")"
  elif delta.has_key(exp[0]):
    result = exp[0] + "(" + formatExp(psi, delta, omega, exp[1][0])
    for p in exp[1][1:]:
      result += "," + formatExp(psi, delta, omega, p)
    return result + ")"
  elif exp[0] == "if":
    result = "if " + exp[1] + "?(" + formatExp(psi, delta, omega, exp[2][0])
    for p in exp[2][1:]:
      result += "," + formatExp(psi, delta, omega, p)
    return result + ") then " + formatExp(psi, delta, omega, exp[3]) + " else " + formatExp(psi, delta, omega, exp[4])
  else:
    return exp[0]

def printParams(n, params):
  printf("I(delta, omega%u, %s)", n, formatExp(psi, delta, omega, params[0]));
  for p in params[1:]:
    printf(",I(delta, omega%u, %s)", n, formatExp(psi, delta, omega, p));
  printf(")\n")

def I(indent, psi, delta, (omega, n), exp):
  # CONDITIONAL
  if exp[0] == "if":
    printf("%sNebenrechnung:\n%sI(delta, omega%u, %s)\n%s= %s?(", " " * (indent + 2), " " * (indent + 4), n, formatExp(psi, delta, omega, exp[1:3]), " " * (indent + 4), exp[1])
    printParams(n, exp[2])
    if (psi.hasPredicate(exp[1])):
      params = []
      for param in exp[2]:
        printf("%sI(delta, omega%u, %s)\n", " " * (indent + 6), n, formatExp(psi, delta, omega, param));
        params.append(I(indent + 6, psi, delta, (omega, n), param))
      if (psi.processPredicate(exp[1], params)):
        printf("%s= %s?(%s)\n%s= T\n%s = I(delta,omega%u,%s)\n", " " * (indent + 4), exp[1], `params`[1:-1], " " * (indent + 4), " " * indent, n, formatExp(psi, delta, omega, exp[3]))
        return I(indent, psi, delta, (omega, n), exp[3])
      else:
        printf("%s= %s?(%s)\n%s= F\n%s= I(delta,omega%u,%s)\n", " " * (indent + 4), exp[1], `params`[1:-1], " " * (indent + 4), " " * indent, n, formatExp(psi, delta, omega, exp[4]))
        return I(indent, psi, delta, (omega, n), exp[4])
  # CONSTANT
  elif psi.hasConstant(exp[0]):
    result = psi.getConstant(exp[0])
    printf("%s= %s\n", " " * indent, result)
    return result
  # VARIABLE
  elif omega.has_key(exp[0]):
    result = omega[exp[0]]
    printf("%s= omega%u(%s)\n%s= %s\n", " " * indent, n, exp[0], " " * indent, result);
    return result
  # DATATYPE FUNCTION
  elif psi.hasFunction(exp[0]):
    printf("%s= %s(", " " * indent, exp[0])
    printParams(n, exp[1])
    params = []
    for param in exp[1]:
      printf("%sI(delta, omega%u, %s)\n", " " * (indent + 2), n, formatExp(psi, delta, omega, param));
      params.append(I(indent + 2, psi, delta, (omega, n), param))
    result = psi.processFunction(exp[0], params)
    printf("%s= %s\n", " " * indent, result)
    return result
  # FUNCTION
  elif delta.has_key(exp[0]):

    # fill new omega environment
    printf("%sNeues Environment (omega%u):\n", " " * (indent + 2), n + 1)
    new_omega = dict()
    paramNames = delta[exp[0]][0]
    paramList = exp[1]
    for i in range(0, len(paramNames)):
      printf("%somega%u(%s)\n", " " * (indent + 4), n + 1, paramNames[i]);
      printf("%s= I(delta, omega%u, %s)\n", " " * (indent + 4), n, formatExp(psi, delta, omega, paramList[i]))
      new_omega[paramNames[i]] = I(indent + 4, psi, delta, (omega, n), paramList[i])
    # call I with implementation of the function and new omega environment
    implementation = delta[exp[0]][1]
    printf("%s= I(delta,omega%u,%s)\n", " " * indent, n + 1, formatExp(psi, delta, omega, implementation))
    return I(indent, psi, delta, (new_omega, n + 1), implementation)

  else:
    print "Fatal error parsing: ", exp
    exit(-1)

omega = dict()

psi = Integer()
(exp, delta) = parse(["E(x) = if eq?(x,null) then null else add(x,E(sub(x,eins)))", "E(zwei)"])
printf("I(delta,omega0,%s)\n", formatExp(psi, delta, omega, exp))
printf("Result: %s\n", I(0, psi, delta, (omega, 0), exp))
