from optparse import OptionParser

def newtonInterpolate(x, y):

    n = len(x)
    A = [[0.]*n]*(n+1)
    A[0] = x
    A[1] = y

    #print A[xindex][yindex]

    # loop through columns
    for i in range(2, n+1):
        # loop through rows
        for j in range(0, n-i+1):
            # calculate new value depending on the already known (using scheme of divided differences)
            A[i][j] = (A[i-1][j+1] - A[i-1][j]) / (A[0][j+i-1] - A[0][j])

    return A

if __name__ == "__main__":

    # init command line parser
    parser = OptionParser()
    parser.add_option("-x", "--x", dest="x", help="array with x values")
    parser.add_option("-y", "--y", dest="y", help="array with y values")
    (options, args) = parser.parse_args()

    if not options.x or not options.y:
        parser.print_help()
    else:
        print newtonInterpolate(eval(options.x), eval(options.y))
