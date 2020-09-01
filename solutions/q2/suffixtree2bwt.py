# Ho Yi Ping
# This file contains all the code for question 2 (BWT). Run the file from 
# commnad line via: python suffixtree2bwt.py <text_file>. <text_file> should be relative to the 
# location of the script instead of the shell's working directory. This program will write its 
# output to a file named 'output_bwt.txt' in the same directory as the script. 

import os, sys
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)
sys.path.append('..')
from ukkonen import ukkonen
from utils import read_file


def bwt_rec(node, string, length, output):
    '''
    Build BWT output by traversing the given suffix tree in lexicographical DFS order.
        node:   Current node under consideration.
        string: Input string to BWT prepended with the termination character.
        length: Number of characters deep into the current branch.
        output: Pointer to the output list.
        Time:   O(n)
        Space:  O(n)
            where:
            n = length of 'string'
    '''
    edges = list(filter(lambda edge: edge is not None, node.edges))  # < |ALPHABET SIZE|
    if len(edges) == 0:
        output.append(string[-length])  # |output| <= |string|
        return output
    for edge in edges:
        edge_len = edge.end - edge.start + 1
        bwt_rec(edge, string, length + edge_len, output)
    return output


def bwt(string):
    '''
    Returns the BWT output of the given string by creating its suffix tree.
        string: String of characters as input to BWT
        Time:   O(n)
        Space:  O(n)
            where:
            n = length of 'string'
    '''
    tree = ukkonen(string, termination='$')
    output = bwt_rec(tree, '$' + string, 0, [])
    return output


if __name__ == '__main__':
    text_fp = sys.argv[1]
    text = read_file(text_fp)
    bwt_string = bwt(text)
    with open('./output_bwt.txt', 'w') as output_file:
        output_file.write(''.join(bwt_string))
