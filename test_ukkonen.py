from timeit import default_timer as timer
import multiprocessing as mp
from ukkonen import ukkonen


def check_suffix_range(root, string, start=0, end=-1):
    n = len(string)
    if end == -1:
        end = n
    mismatches = 0
    errors = 0
    for i in range(start, end):
        # check substring string[i:]
        print(f'\rSubstring {i+1}/{end}', end='')
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
    import cProfile

    text_file = './reference.txt'

    print('Reading text from', text_file)
    with open(text_file) as f:
        text = f.read()
    text = text[:100000]
    if len(text) < 100:
        print(text, len(text))
    
    print('Profiling')
    cProfile.run('ukkonen(text)')
    print()

    print('Building suffix tree')
    time_taken = timer()
    tree = ukkonen(text, disp='None')
    print(f'Suffix tree built in {round(timer() - time_taken, 4)} seconds')

    start, end = None, None
    print(f'Checking suffixes starting from {start} to {end}')
    time_taken = timer()
    check_suffix_range(tree, text + '$')
    print(f'Checked suffix tree in {round(timer() - time_taken, 4)} seconds')
