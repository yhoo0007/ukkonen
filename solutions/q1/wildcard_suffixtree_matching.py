# Ho Yi Ping
# This file contains all the code for question 1 (Wildcard Matching). Run
# the file from commnad line via: python wildcard_suffixtree_matching.py <text_file> <pattern_file>
# <text_file> and <pattern_file> should be relative to the location of the script instead of the 
# shell's working directory. This program will write its output to a file named
# 'output_wildcard_matching.txt' in the same directory as the script. 

import os, sys
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)
sys.path.append('..')
from ukkonen import ukkonen
from utils import read_file


def get_leaves(node, leaves):
    '''
    Recursively adds leaves of the given node to the given list.
        node:   Current node under consideration.
        leaves: Output list of leaves.
        Time:   O(n)
        Space:  O(n)
            where:
            n = number of nodes in tree/subtree
    '''
    edges = list(filter(lambda e: e is not None, node.edges))
    if len(edges) ==  0:  # base case: node is a leaf
        leaves.append(node)
        return leaves
    for edge in edges:
        get_leaves(edge, leaves)
    return leaves


def compare_edge(edge, pat, string, index):
    '''
    Checks whether an edge should be considered or not when traversing for string matching. Also
    matches '?' as a wildcard which matches any character.
        edge:   The current edge under consideration.
        pat:    The pattern to be matched.
        string: The input string.
        index:  The current index in the pattern being matched.
        Time:   O(n)
        Space:  O(n)
            where:
            n = length of 'string'
    '''
    edge_len = edge.end - edge.start + 1
    pat_rem = len(pat) - index
    for i in range(min(edge_len, pat_rem)):  # check characters on the given edge
        pat_char = pat[index + i]
        string_char = string[edge.start + i]
        if pat_char != string_char and not (pat_char == '?' and string_char != '$'):
            return False
    return edge


def wildcard_matching_rec(node, pat, string, index, leaves):
    '''
    Recursive function for matching pattern with string by traversing suffix tree according to 
    characters in pattern. If the first character out of a node is a wildcard (?), every outgoing
    edge will be considered. Once a full match has been found, all leaves from the current node are
    retrieved. The leaves will contain the indices at which the pattern occurs in the string.
        node:   Current node under consideration.
        pat:    The pattern to be matched.
        string: The input string.
        index:  The current index in the pattern.
        leaves: Cumulative list of leaves.
        Time:   O(n)
        Space:  O(n)
            where:
            n = 
    '''
    if index >= len(pat):
        return get_leaves(node, leaves)
    pat_char = pat[index]
    edges = node.edges if pat_char == '?' else [node.edges[ord(pat_char)]]
    for edge in edges:
        if edge is not None and compare_edge(edge, pat, string, index):
            wildcard_matching_rec(
                edge,
                pat,
                string,
                index + edge.end - edge.start + 1,
                leaves
            )
    return leaves


def wildcard_matching(pat, string, tree=None):
    '''
    Helper function for calling the recursive wildcard matching function.
        string: The input string.
        pat:    The pattern to be matched.
    '''
    if len(pat) == 0:
        return [0]
    if tree is None:
        tree = ukkonen(string, termination='$')
    occurrances = [leaf.id for leaf in wildcard_matching_rec(tree, pat, string + '$', 0, [])]
    return occurrances


if __name__ == '__main__':
    text_fp, pat_fp = sys.argv[1:]
    text = read_file(text_fp)
    pat = read_file(pat_fp)
    occurrances = wildcard_matching(pat, text)
    with open('./output_wildcard_matching.txt', 'w') as output_file:
        output_file.writelines(map(lambda occ: str(occ + 1) + '\n', occurrances))
