# Ho Yi Ping
# Test suite for question 1 (Wildcard matching).

import unittest
import re
import random
from wildcard_suffixtree_matching import wildcard_matching

import os, sys
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)
sys.path.append('..')
from ukkonen import ukkonen


def load_test_files():
    with open('./test/reference.txt') as f:
        text = f.read()
    with open('./test/pattern1.txt') as f:
        pat1 = f.readlines()
    with open('./test/pattern2.txt') as f:
        pat2 = f.readlines()
    return text, pat1, pat2


def insert_random_wildcards(string):
    pattern = list(string.strip())
    for _ in range(random.randint(0, len(pattern)-1)):
        pattern[random.randint(0, len(pattern)-1)] = '?'
    pattern = ''.join(pattern)
    re_pattern = ''.join(['.' if c == '?' else c for c in pattern])
    return pattern, re_pattern


class TestWildcardMatching(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        print('Building tree')
        self.text, self.pat1, self.pat2 = load_test_files()
        self.tree = ukkonen(self.text)

    def subcase(self, n, actual, expected):
        print('Subcase', n)
        self.assertEqual(actual, expected)
    
    def test_empty(self):
        print('\nTest Empty')
        res = wildcard_matching('', '')
        res.sort()
        self.subcase(1, res, [0])
    
    def test_empty_text(self):
        print('\nTest Empty Text')
        res = wildcard_matching('abc', '')
        res.sort()
        self.subcase(1, res, [])
        res = wildcard_matching('aaa', '')
        res.sort()
        self.subcase(2, res, [])
        res = wildcard_matching('aa?', '')
        res.sort()
        self.subcase(3, res, [])

    def test_empty_pat(self):
        print('\nTest Empty Pat')
        res = wildcard_matching('', 'abc')
        res.sort()
        self.subcase(1, res, [0])
        res = wildcard_matching('', 'aaa')
        res.sort()
        self.subcase(2, res, [0])

    def test_match_prefix(self):
        print('\nTest Match Prefix')
        res = wildcard_matching('aa', 'aab')
        res.sort()
        self.subcase(1, res, [0])
        res = wildcard_matching('ab', 'abb')
        res.sort()
        self.subcase(2, res, [0])
        res = wildcard_matching('a?', 'abb')
        res.sort()
        self.subcase(3, res, [0])
        res = wildcard_matching('??', 'aba')
        res.sort()
        self.subcase(4, res, [0, 1])
        res = wildcard_matching('?b', 'aba')
        res.sort()
        self.subcase(5, res, [0])
    
    def test_match_suffix(self):
        print('\nTest Match Suffix')
        res = wildcard_matching('ba', 'aba')
        res.sort()
        self.subcase(1, res, [1])
        res = wildcard_matching('aa', 'baa')
        res.sort()
        self.subcase(2, res, [1])
        res = wildcard_matching('b?', 'aba')
        res.sort()
        self.subcase(3, res, [1])
        res = wildcard_matching('??', 'aba')
        res.sort()
        self.subcase(4, res, [0, 1])
        res = wildcard_matching('?a', 'aba')
        res.sort()
        self.subcase(5, res, [1])
    
    def test_match_exact(self):
        print('\nTest Match Exact')
        res = wildcard_matching('aba', 'aba')
        res.sort()
        self.subcase(1, res, [0])
        res = wildcard_matching('aaa', 'aaa')
        res.sort()
        self.subcase(2, res, [0])
        res = wildcard_matching('a', 'a')
        res.sort()
        self.subcase(3, res, [0])
        res = wildcard_matching('?', 'a')
        res.sort()
        self.subcase(4, res, [0])
        res = wildcard_matching('???', 'aba')
        res.sort()
        self.subcase(5, res, [0])
        res = wildcard_matching('a?a', 'aba')
        res.sort()
        self.subcase(6, res, [0])

    def test_match_middle(self):
        print('\nTest Match Middle')
        res = wildcard_matching('aa', 'aaaaa')
        res.sort()
        self.subcase(1, res, [0, 1, 2, 3])
        res = wildcard_matching('aa', 'baab')
        res.sort()
        self.subcase(2, res, [1])
        res = wildcard_matching('bac', 'cbacd')
        res.sort()
        self.subcase(3, res, [1])
        res = wildcard_matching('b?c', 'cbacd')
        res.sort()
        self.subcase(4, res, [1])
        res = wildcard_matching('b??', 'cbacd')
        res.sort()
        self.subcase(5, res, [1])
        res = wildcard_matching('??c', 'cbacd')
        res.sort()
        self.subcase(6, res, [1])
        res = wildcard_matching('?a?', 'cbacd')
        res.sort()
        self.subcase(7, res, [1])

    def test_pat1(self):
        print('\nTest Pat 1')
        # test all patterns in pat1
        for index, pat in enumerate(self.pat1):
            if index % 10 == 0:
                print(f'{index}/{len(self.pat1)}')
            expected = [m.start() for m in re.finditer(f'(?={pat.strip()})', self.text)]
            try:
                actual = wildcard_matching(pat.strip(), self.text, self.tree)
                actual.sort()
            except KeyboardInterrupt as e:
                print(index, pat)
                raise e
            try:
                self.assertEqual(actual, expected)
            except AssertionError as e:
                print(index, pat)
                raise e
        print(f'{len(self.pat1)}/{len(self.pat1)}')
    
    def test_pat2(self):
        print('\nTest Pat 2')
        # test all patterns in pat2
        for index, pat in enumerate(self.pat2):
            if index % 10 == 0:
                print(f'{index}/{len(self.pat2)}')
            expected = [m.start() for m in re.finditer(f'(?={pat.strip()})', self.text)]
            try:
                actual = wildcard_matching(pat.strip(), self.text, self.tree)
                actual.sort()
            except KeyboardInterrupt as e:
                print(index, pat)
                raise e
            try:
                self.assertEqual(actual, expected)
            except AssertionError as e:
                print(index, pat)
                raise e
        print(f'{len(self.pat2)}/{len(self.pat2)}')

    def test_pat1_wildcard(self):
        print('\nTest Pat 1 Randomized Wildcards')
        random.seed(1)
        # test all patterns in pat1 with random wildcard(s) inserted
        for index, pat in enumerate(self.pat1):
            if index % 10 == 0:
                print(f'{index}/{len(self.pat1)}')
            pattern, re_pattern = insert_random_wildcards(pat)
            expected = [m.start() for m in re.finditer(f'(?={re_pattern})', self.text)]
            try:
                actual = wildcard_matching(pattern, self.text, self.tree)
                actual.sort()
            except KeyboardInterrupt as e:
                print(index, pattern, re_pattern)
                raise e
            try:
                self.assertEqual(actual, expected)
            except AssertionError as e:
                print(index, pattern, re_pattern)
                raise e
        print(f'{len(self.pat1)}/{len(self.pat1)}')

    def test_pat2_wildcard(self):
        print('\nTest Pat 2 Randomized Wildcards')
        random.seed(2)
        # test all patterns in pat1 with random wildcard(s) inserted
        for index, pat in enumerate(self.pat2):
            if index % 10 == 0:
                print(f'{index}/{len(self.pat2)}')
            pattern, re_pattern = insert_random_wildcards(pat)
            expected = [m.start() for m in re.finditer(f'(?={re_pattern})', self.text)]
            try:
                actual = wildcard_matching(pattern, self.text, self.tree)
                actual.sort()
            except KeyboardInterrupt as e:
                print(index, pattern, re_pattern)
                raise e
            try:
                self.assertEqual(actual, expected)
            except AssertionError as e:
                print(index, pattern, re_pattern)
                raise e
        print(f'{len(self.pat2)}/{len(self.pat2)}')


if __name__ == '__main__':
    op = input('1: unit test\n2: profile\n3: time\n4: scalability\n> ')

    if op == '1':
        unittest.main(failfast=True)

    elif op == '2':
        import cProfile
        test_pat = '?TT??TAT'
        text, _, _ = load_test_files()
        cProfile.run('wildcard_matching(test_pat, text)')

    elif op == '3':
        from timeit import default_timer as timer
        text, pat, _ = load_test_files()
        print(f'Timing construction + {len(pat)} queries')
        time_taken = timer()
        tree = ukkonen(text)
        for test_pat in pat:
            wildcard_matching(test_pat, text, tree)
        time_taken = timer() - time_taken
        print('Time taken:', time_taken)

    elif op == '4':
        raise NotImplementedError
