import numpy as np
import scipy.optimize as sciopt

target=142
V=np.array([173.3, 5678.8,67898.98, 67898.0, 678987.0, 9876.87, 7659.9 ])
C=np.array([0.1,0.2,0.56,0.56,0.22,0.35,0.21])
L=np.array([1,1,0,0,0,0,1])
init_wts=np.array([0,0,0,0,0,0,0])

def min_cost(wts):
    return np.dot(C,np.multiply(wts,V))

def constraint1(wts):
    return np.dot(wts,V)-target

def constraint2(wts):
    return 0.2*target - np.dot(L,np.multiply(wts,V))

cons1 = ({'type': 'eq','fun': constraint1})
cons2 = ({'type': 'ineq','fun': constraint2})

bnds = tuple((0,1) for wts in range(len(V)))

sol =sciopt.minimize(min_cost, init_wts, method ='SLSQP', bounds=bnds, constraints=[cons1,cons2])
print(sol)