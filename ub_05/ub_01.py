import pylab
import scipy.interpolate
import scipy.optimize

# fit-functions
def linFit(args):
    err = []
    for i in range(len(x)):
        funcVal = args[0] + args[1]*x[i]
	err.append(y[i] - funcVal)
    return err

def cubicFit(args):
    err = []
    for i in range(len(x)):
        funcVal = args[0] + args[1]*x[i] + args[2]*(x[i]**2) + args[3]*(x[i]**3)
	err.append(y[i] - funcVal)
    return err

def fourFit(args):
    err = []
    for i in range(len(x)):
        funcVal = args[0] + args[1]*x[i] + args[2]*(x[i]**2) + args[3]*(x[i]**3) + args[4]*(x[i]**4)
	err.append(y[i] - funcVal)
    return err

# data
x = range(1, 11)# Jahr (+2000)
y = [399621, 374449, 360688, 382339, 410985, 423810, 432599, 438087, 433820, 445479]# bruttoumsatz in 1000 CHF

pylab.plot(x, y, 'ro')

# basisindikator 2011
bi = .15*(sum(y[7:11])/3)
print "basisindikator: " + str(bi)
pylab.plot(11, bi/.15, 'xr')# bruttoerfolg, der fuer die berechnung des bi verwendet wird
#pylab.plot(11, bi, '*b')# tatsaechlicher basisindikator

# lagrange interpolation
yLagrange =  scipy.interpolate.lagrange(x, y)
xExact = scipy.arange(1,12,.1)
#pylab.plot(xExact, [yLagrange(xVal) for xVal in xExact], "b")

# spline interpolation
spline = scipy.interpolate.UnivariateSpline(x, y)
#pylab.plot(xExact, spline(xExact), "g")

# least square fit (linear)
linFitParams = scipy.optimize.leastsq(linFit, [0, 0])[0];
pylab.plot(xExact, linFitParams[0] + linFitParams[1]*xExact, "b")

# least square fit (cubic)
dubicFitParams = scipy.optimize.leastsq(cubicFit, [0, 0, 0, 0])[0];
#pylab.plot(xExact, dubicFitParams[0] + dubicFitParams[1]*xExact + dubicFitParams[2]*(xExact**2) + dubicFitParams[3]*(xExact**3), "y")

# least square fit (4th grade)
fourFitParams = scipy.optimize.leastsq(fourFit, [0, 0, 0, 0, 0])[0];
pylab.plot(xExact, fourFitParams[0] + fourFitParams[1]*xExact + fourFitParams[2]*(xExact**2) + fourFitParams[3]*(xExact**3) + fourFitParams[4]*(xExact**4), "m")

# basisindikator 2011 approximiert
biApprox = .15*(sum(y[8:11], fourFitParams[0] + fourFitParams[1]*11 + fourFitParams[2]*(11**2) + fourFitParams[3]*(11**3) + fourFitParams[4]*(11**4))/3)
print "basisindikator approximiert: " + str(biApprox)
pylab.plot(11, biApprox/.15, 'xm')# bruttoerfolg, der fuer die berechnung des bi verwendet wird
#pylab.plot(11, biApprox, '*m')# tatsaechlicher basisindikator

# show plot
pylab.show()

