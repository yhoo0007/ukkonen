import sys
from timeit import default_timer as timer
from utils import *


class End:
    '''
    Object for representing the global 'end' pointer in Ukkonen's algorithm. In essence this class
    is a pointer to an integer.
    '''
    def __init__(self, n=0):
        self.n = n
    
    def __add__(self, other):
        return self.n + other
    
    def __radd__(self, other):
        return other + self.n
    
    def __sub__(self, other):
        return self.n - other
    
    def __rsub__(self, other):
        return other - self.n

    def __repr__(self):
        return 'E'
    
    def __gt__(self, other):
        return self.n > other
    
    def __ge__(self, other):
        return self.n >= other
    
    def __eq__(self, other):
        return self.n == other
    
    def __le__(self, other):
        return self.n <= other
    
    def __lt__(self, other):
        return self.n < other


class Node:
    '''
    Internal nodes of a suffix tree. Contains an additional 'link' attribute to represent the
    suffix links in Ukkonen's algorithm.
    '''
    def __init__(self, start, end, link, id):
        self.start = start
        self.end = end
        self.link = link  # suffix link for use in Ukkonen's algorithm
        self.edges = [None] * 128  # allocate space for ASCII characters 0 - 127
        self.id = id

    def __str__(self):
        return str(self.id) if self.id is not None else ''

    def __repr__(self):
        return f'Node {self.id}'


class Active:
    '''
    Data class which implements a pointer for a suffix tree. Primarily used to store the active
    point in Ukkonen's algorithm.
    '''
    def __init__(self, node, edge=-1, length=0):
        self.node = node
        self.edge = edge
        self.length = length

    def __str__(self):
        return f'{self.node} {self.edge} {self.length}'

    def __repr__(self):
        return f'{self.node} {self.edge} {self.length}'


def next_char(current_char, string, active):
    '''
    Returns the next char from the active point.
        current_char:   The character at the active point.
        string      :   The input string.
        active      :   Active object representing the active point.
        Time:   O(n)
        Space:  O(1)
            where:
            n = active length
    '''
    while True:
        active_chr_idx = ord(string[active.edge])
        node = active.node.edges[active_chr_idx]
        node_length = node.end - node.start
        if node_length >= active.length:  # character is in current edge
            return string[node.start + active.length]
        if node_length + 1 == active.length:  # character is right after current edge
            return current_char if node.edges[ord(current_char)] is not None else None
        active.node = node
        active.length = active.length - node_length - 1
        active.edge = active.edge + node_length + 1


def ukkonen(string, termination='$', disp=''):
    '''
    Ukkonen's algorithm for creating a suffix tree of the given string.
        string:         String to generate suffix tree for.
        termination:    Unique character that is not found in 'string'. Used as termination
                        character.
        disp:           Suffix tree display mode. 'Phase' shows the suffix tree at each phase,
                        'Final' shows the final suffix tree. Must have matplotlib and networkx
                        installed.
        Time: O(n)
        Space: O(n)
            where:
            n = length of 'string'
    '''
    # deal with 'disp' arg
    disp = disp.casefold()
    if disp == 'phase':
        disp = 1
    elif disp == 'final':
        disp = 2
    
    string += termination
    end = End()  # global 'end' pointer
    node_id = 0  # a simple incremental ID given to nodes when they are created
    root = Node(1, 0, link=None, id=node_id)
    node_id += 1
    active = Active(root)  # object to represent the active point
    remaining = 0  # indicates the number of suffixes to add
    n = len(string)
    for i in range(n):  # phases 0 to n
        prev_node = None
        end.n = i
        remaining += 1
        current_char = string[i]
        current_char_idx = ord(current_char)
        while remaining > 0:  # add the required suffixes for the current phase
            if active.length == 0:
                node = active.node.edges[current_char_idx]
                if node is not None:  # rule 3 showstopper
                    active.edge = node.start
                    active.length += 1  # update active point
                    break
                else:  # rule 2 create new leaf at root
                    root.edges[current_char_idx] = Node(i, end, root, id=-remaining + i + 1)
                    remaining -= 1
            else:
                ch = next_char(current_char, string, active)
                node = active.node.edges[ord(string[active.edge])]
                if ch == current_char:  # rule 3 showstopper
                    if prev_node is not None:
                        prev_node.link = node
                    node_length = node.end - node.start  # update active point
                    if node_length < active.length:
                        active.node = node
                        active.length = active.length - node_length
                        active.edge = node.edges[current_char_idx].start
                    else:
                        active.length += 1
                    break
                # rule 2
                # if ch is not None means ch is in an edge, hence we need to split the edge and 
                # create a new internal node
                elif ch is not None:
                    new_node = Node(node.start, node.start + active.length - 1, root, id=node_id)
                    node_id += 1
                    node.start += active.length
                    new_node.edges[ord(string[new_node.start + active.length])] = node
                    active.node.edges[ord(string[new_node.start])] = new_node
                    node = new_node
                # create new leaf at node
                node.edges[current_char_idx] = Node(i, end, root, id=-remaining + i + 1)
                if prev_node is not None:
                    prev_node.link = node
                prev_node = node
                if active.node is not root:  # update active point
                    active.node = active.node.link
                else:
                    active.edge += 1
                    active.length -= 1
                remaining -= 1
        if disp == 1:
            draw_tree(root, string, title=f'Phase {i}')
    if disp == 2:
        draw_tree(root, string, title='Final')
    return root


if __name__ == '__main__':
    text_file = sys.argv[1]
    text = read_file(text_file)
    print('Text len:', len(text))

    print('Building tree')
    time_taken = timer()
    tree = ukkonen(text, disp='None')
    print(f'Suffix tree built in {round(timer() - time_taken, 4)} seconds')

    # size = get_size(tree)
    # print(f'Total tree size: {size} bytes')
