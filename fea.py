#!/usr/bin/python3

import matplotlib.pyplot as plt
import matplotlib.colors as colors
import numpy as np
import benchmark

class Gene():
    def __init__(self, low, high, shape=(1,2), resolution=10, values=None):
        self.binaries=np.random.randint(low=0, high=2**resolution, size=shape)
        if values is not None:
            self.binaries=values
        self.resolution=resolution
        self.low=low
        self.high=high
        self.shape=shape
        self.range=high-low

    # map 0-2**resolution to low-high
    # i.e., translate the binary value to a value between low-high 
    def convert(self, value:int):
        return self.low+float(value*self.range)/float(2**self.resolution - 1)

    # serialize the genome to a binary string
    def serialize(self):
        t=0
        for i in self.binaries:
            for j in i:
                t=t<<self.resolution
                t+=j
        return t

    # deserialize the binary to the genome
    def deserialize(self, binary):
        shape=self.shape
        t=binary
        v=np.zeros(shape, dtype=self.binaries.dtype)
        for i in  reversed(range(0,shape[0])):
            for j in reversed(range(0,shape[1])):
                v[i][j]=t & (1 << self.resolution) - 1
                t=t>>self.resolution
        return Gene(self.low, self.high, self.shape, self.resolution, v)

    # returns the maximum size of the binary string
    def binarysize(self):
        return (2**self.resolution)*self.shape[0]*self.shape[1]

    # this will translate the genome into real world coordinates
    def trueValues(self):
        v=np.zeros(self.shape)
        for i in range(0,self.shape[0]):
            for j in range(0,self.shape[1]):
                v[i][j]=self.convert(self.binaries[i][j])
        return v

    # definition for crossover
    def crossover(self, g):
        binclone=bin(self.serialize()).split('b')[1]
        left=binclone[0:int(binclone.__len__()/2)]
        bing=bin(g.serialize()).split('b')[1]
        right=bing[int((binclone.__len__()+1)/2):bing.__len__()]
        left+=right
        return self.deserialize(int(left))

    # definition for mutation
    def mutate(self):
        bitstring=bin(self.serialize()).split('b')[1]
        mutpoint=np.random.randint(bitstring.__len__())
        mutatedString=bitstring[0:mutpoint]
        mutatedString+=str(np.random.randint(0,2))
        mutatedString+=bitstring[mutpoint+1:bitstring.__len__()]
        return self.deserialize(int(mutatedString))

    def __str__(self):
        return "bin:{}, true:{}".format(self.binaries.__str__(), self.trueValues())

    def copy(self):
        return Gene(self.low, self.high, self.shape, self.resolution, self.binaries)

population_size=32
low=-5
high=5
population=list([Gene(low,high) for i in range(population_size)])

number_of_generations=1000
number_of_maters=8
mutation_probability=0.01
crossover_probability=0.01

X = np.arange(-5.12, 5.12, 0.1)
Y = np.arange(-5.12, 5.12, 0.1)
X, Y = np.meshgrid(X, Y)
Z = benchmark.rastrigin_space(X,Y)
fitness=benchmark.square_cost_function

plt.pcolormesh(X,Y,Z, cmap=plt.get_cmap('gnuplot'), norm=colors.PowerNorm(gamma=0.8))

def plotpoint(t,color='white', marker='o'):
    plt.scatter(t[0], t[1], c=color, marker=marker)

import random
plt.ion()
for g in range(number_of_generations):
    print("Generation",g,"/", number_of_generations)
    plt.clf()
    plt.pcolormesh(X,Y,Z, cmap=plt.get_cmap('gnuplot'), norm=colors.PowerNorm(gamma=0.8))
    for i, p in enumerate(population):
        # Plot all peeps
        t=p.trueValues()[0]
        plotpoint(t)

    # Sort by fitness
    population.sort(key=lambda x: fitness(x.trueValues()[0]))
    # Plot best peeps to mate in green
    for i in range(number_of_maters):
        plotpoint(population[i].trueValues()[0], color='green')
    for i in range(population_size):
        if np.random.uniform()<crossover_probability:
            # mate between two random winners
            population[i]=population[i].crossover(population[np.random.randint(number_of_maters+1)])
        if np.random.uniform()<mutation_probability:
            # mutate the genome
            population[i]=population[i].mutate()
    plt.show()
    plt.pause(0.001)
plt.draw()
