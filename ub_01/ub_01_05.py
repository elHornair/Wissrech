#!/usr/bin/python

from optparse import OptionParser
import pickle, math, re


def compress_file(input_path, output_path):
    '''compresses a file using the huffman compression'''
    
    #read the file content
    input_file = open(input_path, 'r')
    text = input_file.read()
    input_file.close()
    dictionary = build_dictionary(text, 2)
    compressed = compress(text, dictionary)
    dict_rep = serialize_dict(dictionary)
    
    file = open(output_path, 'wb')
    file.write(dict_rep + compressed)
    file.close()
    
    
def decompress_file(input_path, output_path):
    '''extracts a file using the huffman compression'''
    
    #read the file content
    input_file = open(input_path, 'r')
    compressed = input_file.read()
    input_file.close()
    dictionary = unserialize_dict(compressed)
    
    #invert dictionary for easier access - also calculate the shortest and longest code
    inv_dictionary = []
    min_code_length = None
    max_code_length = None
    for char, code in dictionary.iteritems():
        inv_dictionary.append((code, char))
        code_length = len(code)
        if min_code_length == None or code_length < min_code_length:
            min_code_length = code_length
        if max_code_length == None or code_length > max_code_length:
            max_code_length = code_length
    
    inv_dictionary.sort(key=lambda tup: tup[0], cmp=lambda x,y: cmp(len(x), len(y)))
    
    compressed = compressed[len(serialize_dict(dictionary)):]
    
    binaryText = ''
    for char in compressed[:-1]:
        binaryText += bin(ord(char))[2:].zfill(8)
    binaryText += bin(ord(compressed[-1]))[2:]
        
    text = ''
    string_offset = 0

    while string_offset < len(binaryText):
        char = ''
        tmp = binaryText[string_offset:string_offset + max_code_length]
        code_length = 0
        for entry in inv_dictionary:
            if re.search("^" + entry[0], tmp):
                char = entry[1]
                code_length = len(entry[0])

        if len(char) == 0:
            break
        
        text += char
        string_offset += code_length

    file = open(output_path, 'w')
    file.write(text)
    file.close()
    

def compress(text, dictionary):
    '''compresses the input text with the given dictionary'''
    
    binaryText = ''
    for char in text:
        binaryText += dictionary[char]

    i = 0
    compressed = ''
    while i < len(binaryText) - 8:
        compressed += chr(int(binaryText[i:i+8], 2))
        i += 8
    
    compressed += chr(int(binaryText[i:], 2))

    return compressed
    
    
def serialize_dict(dictionary):
    '''returns a serialized version of the dictionary'''
    
    #serialize the dictionary
    return pickle.dumps(dictionary)
    

def unserialize_dict(compressed):
    '''extracts the dictionary from a compressed file'''
    
    return pickle.loads(compressed)
    

def build_dictionary(text, max_leaves):
    '''builds the dict for the compression'''

    #count appearances of chars
    frequency_dict = {}
    for char in text:
        if frequency_dict.__contains__(char):
            frequency_dict[char] += 1
        else:
            frequency_dict[char] = 1
            
    dictionary = []
    for char, appearances in frequency_dict.items():
        percentage = int(math.floor(100.0 / len(text) * appearances * 100))
        dictionary.append((percentage, char))
    
    dictionary.sort(key=lambda tup: tup[0])

    while len(dictionary) > 1:
        
        #collect leaves
        leaves = []
        weight = 0
        while len(leaves) < max_leaves:
            try:
                leave = dictionary.pop(0)
                weight += leave[0]
                leaves.append(leave)
            except:
                break

        #add node back to dictionary
        dictionary.append((weight, leaves))
        
        #sort it again
        dictionary.sort(key=lambda tup: tup[0])
    
    codes = {}
    def traverse_dictionary(node, code):
        
        if type(node[1]).__name__ == 'list':
            i = 0
            for subnode in node[1]:
                traverse_dictionary(subnode, code + bin(i)[2:])
                i += 1
        else:
            codes[node[1]] = code
    
    traverse_dictionary(dictionary[0], '')
    
    return codes


if __name__ == "__main__":
    '''Compress a file with the huffman compressoin'''
    
    #init command line parser
    usage = "usage: %prog compress/decompress input output"
    parser = OptionParser(usage=usage)
    (options, args) = parser.parse_args()

    if not args[0] in ['compress', 'decompress'] or len(args) < 3:
        parser.print_help()
    else:
        try:
            if args[0] == 'compress':
                compress_file(args[1], args[2])
            else:
                decompress_file(args[1], args[2])
        except Exception as e:
            print e