#!/usr/bin/env python
import sys

def g(y,x, expr):
    y1 = eval(expr)
    return y1

if __name__=='__main__':
    init = int(sys.argv[1]) # the first argument passed to the script
    expr = sys.argv[2]
    print "Result of expression '%s' where x is %d is: %d" % (expr, init, g([0],init,expr))

