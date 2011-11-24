import numpy
import pylab
import mpl_toolkits.mplot3d.axes3d as p3

# base values
delta = 0.1
x = numpy.arange(-5.0, 5.0, delta)
y = numpy.arange(-5.0, 5.0, delta)
X, Y = pylab.meshgrid(x, y)

# functions
Z1 = X**2+Y**2-3 # func1
Z2 = X*Y-1 # func2

# config
fig = pylab.figure()
ax = p3.Axes3D(fig)
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

# plot
ax.plot_surface(X, Y, Z1, alpha=0.5)
ax.plot_surface(X, Y, Z2, alpha=0.5)

pylab.show()
