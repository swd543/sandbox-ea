#!/usr/bin/python3
# Authors - Swapneel, Tom, Arthur
# Import the random module
import random as rnd
import sys

# Define a Vector class
# Realised later-can be more general in dimension :(
# Or simply could have used numpy arrays lol
class Vector():
    def __init__(self,dimensions=2,values=[]):
        self.values=values
        self.dimensions=dimensions
        for _ in range(len(self.values), dimensions):
            self.values.append(0)
        if len(self.values)>dimensions:
            raise ValueError("Values supplied do not match dimension or dimension is negative")
    def __str__(self):
        return self.values.__str__()
    def all_random(self,all_range=[-1,1]):
        self.__init__(self.dimensions,[rnd.uniform(all_range[0], all_range[1]) for i in range(self.dimensions)])
        return self
    def __getitem__(self, key):
        return self.values[key]
    def copy(self):
        return Vector(self.dimensions, self.values.copy())

A=0.6   # Inertia
B=2     # Social constant
C=2     # Cognitive constant

# Define a Particle class
class Point():
    def __init__(self,velocity=Vector().all_random(),position=Vector().all_random(),best_position=Vector().all_random(),best_error=sys.maxsize,values_range=Vector(values=[-2,2])):
        self.velocity=velocity
        self.position=position
        self.best_position=best_position
        self.best_error=best_error
        self.error=best_error
        self.values_range=values_range

    def evaluate(self,costFunction):
        self.error=costFunction(self.position)
        if self.error<self.best_error:
            self.best_position=self.position
            self.best_error=self.error
    
    def update(self, group_best_position, post_update=None):
        # Repeat for all dimensions
        for i in range(self.position.dimensions): 
            # Update velocity first, position later?
            self.velocity.values[i]=A*self.velocity[i]+B*rnd.uniform(0,1)*(self.best_position[i]-self.position[i])+C*rnd.uniform(0,1)*(group_best_position[i]-self.best_position[i])
            self.position.values[i]=self.position[i]+self.velocity[i]
        # Run whatever needs to be updated on the graph, etc
        if post_update!=None: post_update()
    
    def __str__(self):
        return "<P:{}, V:{}, E:{}, BE:{}, BP:{}>".format(self.position, self.velocity, self.error, self.best_error, self.best_position)
        # return "<P:{}, E:{}>".format(self.position,self.error)
        # return "<E:{}>".format(self.error)

import numpy as np
def rosenbrock_space(x,y,a=0,b=1):
    return (a-x)**2+b*((y-x**2)**2)
def rastrigin_space(x,y,a=1):
    return a*2+(x**2-a*np.cos(2*np.pi*x)-a*np.cos(2*np.pi*y))

# Set the space below
# space=rosenbrock_space
space=rastrigin_space

def abs_cost_function(x, f=space):
    return np.abs(f(x[0], x[1]))
def square_cost_function(x, f=space):
    return f(x[0],x[1])**2
    # return np.sum([i**2 for i in x]) 

# Set the cost function below
cost_function=square_cost_function

import matplotlib.pyplot as plt
plt.ion()
X = np.arange(-2, 2, 0.1)
Y = np.arange(-2, 2, 0.1)
X, Y = np.meshgrid(X, Y)
Z = space(X,Y)
plt.pcolormesh(X,Y,Z)
plt.draw()

# Number of particles
N=20
# Maximum iterations
M=20
# Expected error
E=0.0001

points=[Point(velocity=Vector().all_random(), position=Vector().all_random(), best_position=Vector().all_random()) for _ in range(N)]
print([p.position.__str__() for p in points])

for i in range(N):
     print(i,points[i])
best_error=sys.maxsize
group_best_position=Vector()
for _ in range(M):
    plt.clf()
    
    for i in range(N):
        points[i].evaluate(cost_function)
        if points[i].error < best_error:
            group_best_position=points[i].position.copy()
            best_error=points[i].error

    plt.pcolormesh(X,Y,Z, cmap=plt.get_cmap('gnuplot'))
    plt.colorbar()
    plt.scatter([p.position[0] for p in points], [p.position[1] for p in points])
    plt.scatter(group_best_position.values[0], group_best_position.values[1], c='red')
    plt.draw()
    print(group_best_position, best_error)
    print([p.__str__() for p in points])
    for i in range(N):
        points[i].update(group_best_position, None)
    if best_error<=E:
        print("Best error has been found with value", best_error,", terminating!")
        input()
        break
    plt.pause(0.05)
