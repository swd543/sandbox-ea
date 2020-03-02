import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

fig = plt.figure()
ax = fig.gca(projection='3d')

x = np.arange(200)
y = np.arange(200)
x, y = np.meshgrid(x, y)
z = np.zeros((200, 200))

# Create index arrays.
I, J = np.meshgrid(np.arange(200), np.arange(200))

# Calculate distance of all points to center.
dist = np.sqrt((I - 100)**2 + (J - 100)**2)

# Create the peak.
radius = 50
height = 1
curve = np.linspace(0, np.pi, radius*2)
z_peak = [(np.cos(i) + 1) * height / 2 for i in curve]
for cr, h in enumerate(z_peak):
    z = np.where(dist < cr, z, h)

ax.plot_surface(x, y, z, rstride=1, cstride=1, linewidths=0, cmap='terrain')

# Generate points to represent population.
x_ = np.random.randint(0, 200, size=100)
y_ = np.random.randint(0, 200, size=100)
z_ = []
for x, y in zip(x_, y_):
    z_.append(z[x, y])
points = ax.scatter(x_, y_, z_)
plt.show()