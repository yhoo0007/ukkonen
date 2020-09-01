# Ho Yi Ping
# Test suide for question 2 (BWT).

import unittest
from suffixtree2bwt import bwt


def naive_bwt(string):
    s = string + '$'
    prefixes = [s[i:] + s[:i] for i in range(len(s))]
    prefixes.sort()
    return [p[-1] for p in prefixes]


class TestBWT(unittest.TestCase):
    def subcase(self, n, actual, expected):
        print('Subcase', n)
        self.assertEqual(actual, expected)

    def test_empty(self):
        test_string = ''
        print('\nTest Empty')
        self.subcase(1, naive_bwt(test_string), bwt(test_string))

    def test_single(self):
        test_string = 'a'
        print('\nTest Single')
        self.subcase(1, naive_bwt(test_string), bwt(test_string))
        test_string = 'Z'
        self.subcase(2, naive_bwt(test_string), bwt(test_string))

    def test_same(self):
        test_string = 'aaaa'
        print('\nTest Same')
        self.subcase(1, naive_bwt(test_string), bwt(test_string))
        test_string = 'bbbbbbbb'
        self.subcase(2, naive_bwt(test_string), bwt(test_string))

    def test_one(self):
        test_string = 'aaab'
        print('\nTest One')
        self.subcase(1, naive_bwt(test_string), bwt(test_string))
        test_string = 'baaa'
        self.subcase(2, naive_bwt(test_string), bwt(test_string))
        test_string = 'aaba'
        self.subcase(3, naive_bwt(test_string), bwt(test_string))
        test_string = 'abaa'
        self.subcase(4, naive_bwt(test_string), bwt(test_string))

    def test_varied(self):
        import random
        import string
        print('\nTest Random')
        max_string_len = 10000
        num_calls = 100
        print('Max String Length:', max_string_len)
        for i in range(num_calls):
            print(f'\rTest: {i+1}/{num_calls}', end='')
            string_len = random.randint(0, max_string_len)
            test_string = ''.join(random.choices(string.ascii_letters, k=string_len))
            self.assertEqual(naive_bwt(test_string), bwt(test_string))
        print()


if __name__ == '__main__':
    op = input('1: unit test\n2: profile\n3: time\n4: scalability\n> ')

    if op == '1':
        unittest.main(failfast=True)

    elif op == '2':
        import cProfile
        test_string = 'mississippi'
        cProfile.run('bwt(test_string)')

    elif op == '3':
        from timeit import default_timer as timer
        import string, random
        num_calls = 100
        string_len = 1000
        strings = [''.join(random.choices(string.ascii_letters, k=string_len)) for _ in range(num_calls)]
        print(f'Timing {num_calls} calls')
        time_taken = timer()
        for test_string in strings:
            bwt(test_string)
        time_taken = timer() - time_taken
        print('Time taken:', time_taken)
        print('Avg time taken:', time_taken / num_calls)

    elif op == '4':
        raise NotImplementedError
