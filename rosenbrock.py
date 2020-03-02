#!/usr/bin/python3
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 unused import

import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import numpy as np

fig = plt.figure()

# Make data for Rosenbrock function
A=0
B=100
X = np.arange(-1, 1, 0.1)
Y = np.arange(-1, 2, 0.1)
X, Y = np.meshgrid(X, Y)
Z = (A-X)**2+B*((Y-X**2)**2)
# Plot the surface.
plt.pcolormesh(X,Y,Z, cmap=plt.get_cmap('gnuplot'))
plt.scatter(0,0)
plt.colorbar()
plt.show()

