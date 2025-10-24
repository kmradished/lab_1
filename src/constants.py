import operator

OPERATORS = {
    "+": (operator.add, 2),
    "-": (operator.sub, 2),
    "*": (operator.mul, 2),
    "/": (operator.truediv, 2),
    "//": (operator.floordiv, 2),
    "%": (operator.mod, 2),
    "**": (operator.pow, 2),
    "~": (operator.neg, 1),
}
