# Ho Yi Ping
# This file contains all the code for question 3 (Wildcard Matching). Run
# the file from commnad line via: python lcps.py <text_file> <indices_file>. <text_file> and 
# <indices_file> should be relative to the location of the script instead of the shell's working
# directory. This program will write its output to a file named 'output_lcps.txt' in the same 
# directory as the script. 

import os, sys
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)
sys.path.append('..')
from ukkonen import ukkonen
from utils import read_file


def lcps(string, i, j, tree=None):
    '''
    Returns the number of characters that match starting at indices i and j in the given string.
        tree:   Root of the suffix tree of the input string.
        string: The input string.
        i:      First index to start matching at.
        j:      Second index to start matching at.
        Time:   O(n)
        Space:  O(n)
            where:
            n = length of 'string'
    '''
    if not tree:
        tree = ukkonen(string)
    if not isinstance(i, list):
        i = [i]
    if not isinstance(j, list):
        j = [j]
    if len(i) != len(j):
        raise TypeError('number of i and j values must match')
    n = len(string)
    res = []
    for i_, j_ in zip(i, j):
        node = tree
        i_counter = i_
        j_counter = j_
        while j_counter < n and string[i_counter] == string[j_counter]:
            node = node.edges[ord(string[i_counter])]
            edge_len = node.end - node.start + 1
            i_counter += edge_len
            j_counter += edge_len
        result = i_counter - i_
        if node.end == n:
            res.append(result - 1 if result > 0 else 0)
        else:
            res.append(result)
        
    return res[0] if len(i) == 1 else res


if __name__ == '__main__':
    text_fp, indices_fp = sys.argv[1:]
    text = read_file(text_fp)
    
    # Read indices file
    i_values = []
    j_values = []
    with open(indices_fp) as indices_file:
        for line in indices_file:
            i, j = line.strip().split(' ')
            i_values.append(int(i) - 1)
            j_values.append(int(j) - 1)
    
    # Get results and write to file
    results = lcps(text, i_values, j_values)
    to_file = []
    for i, j, res in zip(i_values, j_values, results):
        string = f'{i + 1} {j + 1} {res}\n'
        to_file.append(string)
    with open('./output_lcps.txt', 'w') as output_file:
        output_file.writelines(to_file)
