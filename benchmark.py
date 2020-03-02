import numpy as np
def rosenbrock_space(x,y,a=0,b=1):
    return (a-x)**2+b*((y-x**2)**2)
def rastrigin_space(x,y,a=10):
    return a*2+(x**2-a*np.cos(2*np.pi*x)+(y**2-a*np.cos(2*np.pi*y)))

def abs_cost_function(x, f=rosenbrock_space):
    return np.abs(f(x[0], x[1]))
def square_cost_function(x, f=rosenbrock_space):
    return f(x[0],x[1])**2