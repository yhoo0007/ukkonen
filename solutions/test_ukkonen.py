import cProfile
from timeit import default_timer as timer
import multiprocessing as mp
from ukkonen import ukkonen
from utils import read_file


def check_suffix_range(root, string, start=0, end=-1):
    n = len(string)
    if end == -1:
        end = n
    mismatches = 0
    errors = 0
    for i in range(start, end):
        # check suffix string[i:]
        print(f'\rSuffix: {i+1}/{end}', end='')
        next_node = root.edges[ord(string[i])]
        rel_idx = 0
        try:
            for j in range(i, n):
                if rel_idx > next_node.end - next_node.start:  # get next edge
                    next_node = next_node.edges[ord(string[j])]
                    rel_idx = 0
                if string[j] != string[next_node.start + rel_idx]:
                    mismatches += 1
                    print(f'\nMismatch! {i}\n')
                    break
                rel_idx += 1
        except Exception as e:
            errors += 1
            print(f'\Error! {i} {e}\n')
    
    print(f'\nChecked {end - start} suffixes, found {mismatches} mismatches and {errors} errors')
    return (mismatches, errors)


if __name__ == '__main__':
    string_fp = input('Enter test txt file: ')

    print('Reading string from', string_fp)
    string = read_file(string_fp)

    if len(string) < 100:
        print(f'Text: {string}\nLength: {len(string)}')

    print('Profiling')
    cProfile.run('ukkonen(string)')
    print()

    print('Building suffix tree')
    time_taken = timer()
    tree = ukkonen(string, disp='None')  # change disp argument to 'Final' to view final tree
    print(f'Suffix tree built in {round(timer() - time_taken, 4)} seconds')

    # start, end = None, None
    # print(f'Checking suffixes starting from {start} to {end}')
    print('Checking all suffixes')
    time_taken = timer()
    check_suffix_range(tree, string + '$')
    print(f'Checked suffix tree in {round(timer() - time_taken, 4)} seconds')
