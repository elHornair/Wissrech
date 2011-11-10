import pylab
import scipy.optimize

# approximation function
def approxFunc(knownXVals, knownYVals):
    def fourFit(args):
        err = []
        for i in range(len(knownXVals)):
            funcVal = args[0] + args[1]*knownXVals[i] + args[2]*(knownXVals[i]**2) + args[3]*(knownXVals[i]**3) + args[4]*(knownXVals[i]**4)
            err.append(knownYVals[i] - funcVal)
        return err

    return scipy.optimize.leastsq(fourFit, [0, 0, 0, 0, 0])[0];

# polynomial of fourth grade
def fourthGradeFunc(x, params):
    res = []
    for i,xVal in enumerate(x):
        res.append(0.0)
        for j,param in enumerate(params):
	    res[i] += param * (xVal**j)
    return res

# data
x = range(1, 11)# Jahr (+2000)
y = [[399621, 374449, 360688, 382339, 410985, 423810, 432599, 438087, 433820, 445479],# bruttoumsatz in 1000 CHF
     [279358, 273940, 253598, 261585, 275527, 273368, 277057, 308543, 315299, 321227],# zinsgeschaeft: 12%
     [80740, 70641, 72892, 81264, 89675, 97219, 98558, 85065, 73394, 79716],# kommissions und dienstleistungsgeschaeft 18%
     [15824, 12361, 17546, 20295, 27921, 25271, 31709, 30046, 27441, 25562]# handelsgeschaeft: 18%
]
beta = [.15, .12, .18, .18]

pylab.plot(x, y[0], 'ro')
pylab.plot(x, y[1], 'go')
pylab.plot(x, y[2], 'bo')
pylab.plot(x, y[3], 'yo')

# least square fit (4th grade)
xExact = scipy.arange(1,12,.1)

fourFitParams = []
for i in range(4):
    fourFitParams.append(approxFunc(x, y[i]))

approxVals = []
for i in range(4):
    approxVals.append(fourthGradeFunc([11], fourFitParams[i])[0])
    pylab.plot(xExact, fourthGradeFunc(xExact, fourFitParams[i]), "m")


# basisindikator 2011 approximiert
biApprox = beta[0]*(sum(y[0][8:11], approxVals[0])/3)
pylab.plot(11, biApprox, '*m')

# basisindikator 2011 approximiert (gewichtet)
biApproxWeighted = 0.0;
for i in range(1, 4):
    biApproxWeighted += approxVals[i] * beta[i]

for i in range(1, 4):
    biApproxWeighted += y[i][9] * beta[i]
    biApproxWeighted += y[i][8] * beta[i]
    biApproxWeighted += y[i][7] * beta[i]

pylab.plot(11, biApproxWeighted/3, '*b')
print biApproxWeighted/3

# basisindikator vergangene jahre approximiert (gewichtet)
for j in range(2, 10):
    biApproxWeighted = 0.0

    for i in range(1, 4):
        biApproxWeighted += y[i][j] * beta[i]
        biApproxWeighted += y[i][j-1] * beta[i]
        biApproxWeighted += y[i][j-2] * beta[i]

    pylab.plot(j+1, biApproxWeighted/3, '*b')

# show plot
pylab.show()

