from optparse import OptionParser

def encode(data):

    code = []

    for bit in data:
	code.append(bit)

    return code

if __name__ == "__main__":

    # init command line parser
    parser = OptionParser()
    parser.add_option("-i", "--input", dest="input", help="string consisting of 0 and 1")
    (options, args) = parser.parse_args()

    print args

    if not options.input:
        parser.print_help()
    else:
        print encode(options.input)
