from optparse import OptionParser

def encode(data):

    code = []

    for bit in data:
	code.append(int(bit))

    # prefill parity-bits with dummy data
    parity_exp = 0
    while 2**parity_exp < len(code):
        code.insert(2**parity_exp-1, 0)
        parity_exp += 1

    # loop through parity bits and define them
    parity_exp = 0
    while 2**parity_exp < len(code):

        parity_index = 2**parity_exp - 1

        # define start-index for XOR-sum (p1 and p2 are edge-cases)
        if parity_exp == 0: #p1
            start_index = 2
        elif parity_exp == 1: #p2
            start_index = 5
            code[parity_index] = code[2]
        else:
            start_index = parity_index + 1

        # build XOR-sum for each parity-bit
        for interval_index in range(start_index, len(code), 2**(parity_exp + 1)):
            for data_index in range(interval_index, interval_index + parity_exp + 1):
                if len(code) > data_index:
                    code[parity_index] = code[parity_index] ^ code[data_index]

        parity_exp += 1

    return "".join(map(str, code))

if __name__ == "__main__":

    # init command line parser
    parser = OptionParser()
    parser.add_option("-i", "--input", dest="input", help="string consisting of 0 and 1")
    (options, args) = parser.parse_args()

    if not options.input:
        parser.print_help()
    else:
        print encode(options.input)
