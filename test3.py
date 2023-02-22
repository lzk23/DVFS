from __future__ import division
import numpy as np
import math
from scipy.optimize import minimize


def cost(x):
    return -1 * x[0]  + 4 * x[1]

def ineqcons1(x):
    return x[1] - x[0] -1

def ineqcons2(x):
    return  x[0] - x[1]

x0 = (1,4)
bnds = ((-5,5), (-5,5))
con = ({'type':'ineq', 'fun': ineqcons1},{'type':'ineq', 'fun': ineqcons2})
res = minimize(cost, x0, method='SLSQP',  bounds = bnds, constraints=con, options={'maxiter' : 10000000, 'ftol':0.0001 })
print("optimization result",res)

for cons in con:
    print("constraints values for optimized variables", cons['fun'], cons['fun'](res.x), cons['type'])