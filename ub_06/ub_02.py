import numpy as np
import pylab as pl

# data
x = np.arange(-5, 5, 0.001)

# plot functions
pl.plot(x, np.sqrt(3-x**2)) # func1 (part2)
pl.plot(x, -np.sqrt(3-x**2)) # func1 (part2)
pl.plot(x, 1/x) # func1

# config
pl.axis([-5, 5, -5, 5])
pl.ylabel('y-axis')
pl.xlabel('x-axis')

pl.show()
