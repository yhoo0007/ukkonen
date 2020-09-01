# Ho Yi Ping
# Test suite for question 3 (LCPS).

import unittest
from lcps import lcps


def naive(string, i, j):
    n = len(string)
    count = 0
    while j < n and string[i] == string[j]:
        count += 1
        i += 1
        j += 1
    return count


class TestBWT(unittest.TestCase):
    def subcase(self, n, actual, expected):
        print('Subcase', n)
        self.assertEqual(actual, expected)
    
    def test_empty(self):
        test_string = ''
        print('\nTest Empty')
        self.subcase(1, naive(test_string, 0, 0), lcps(test_string, 0, 0))

    def test_single(self):
        test_string = 'a'
        print('\nTest Single')
        self.subcase(1, naive(test_string, 0, 0), lcps(test_string, 0, 0))
        test_string = 'Z'
        self.subcase(2, naive(test_string, 0, 0), lcps(test_string, 0, 0))

    def test_same(self):
        test_string = 'aaaa'
        print('\nTest Same')
        self.subcase(1, naive(test_string, 0, 0), lcps(test_string, 0, 0))
        test_string = 'bbbbbbbb'
        self.subcase(2, naive(test_string, 0, 0), lcps(test_string, 0, 0))
    
    def test_one(self):
        test_string = 'aaab'
        print('\nTest One Diff')
        self.subcase(1, naive(test_string, 0, 0), lcps(test_string, 0, 0))
        test_string = 'baaa'
        self.subcase(2, naive(test_string, 1, 1), lcps(test_string, 1, 1))
        test_string = 'aaba'
        self.subcase(3, naive(test_string, 2, 2), lcps(test_string, 2, 2))
        test_string = 'abaa'
        self.subcase(4, naive(test_string, 3, 3), lcps(test_string, 3, 3))
    
    def test_varied(self):
        import random
        import string
        max_string_len = 10000
        num_tests = 1000
        print('\nTest Random')
        print('Max String Length:', max_string_len)
        for i in range(num_tests):
            print(f'\rTest: {i + 1}/{num_tests}', end='')
            string_len = random.randint(0, max_string_len)
            test_string = ''.join(random.choices(string.ascii_letters, k=string_len))
            test_i = random.randint(0, string_len - 1 if string_len - 1 >= 0 else 0)
            test_j = random.randint(test_i, string_len - 1 if string_len - 1 >= 0 else 0)
            self.assertEqual(naive(test_string, test_i, test_j), lcps(test_string, test_i, test_j))
        print()


if __name__ == '__main__':
    op = input('1: unit test\n2: profile\n3: time\n4: scalability\n> ')
    
    if op == '1':
        unittest.main(failfast=True)

    elif op == '2':
        import cProfile
        test_string = 'mississippi'
        cProfile.run('lcps(test_string, 1, 4)')

    elif op == '3':
        from timeit import default_timer as timer
        import string, random
        num_calls = 100
        string_len = 10000
        strings = [''.join(random.choices(string.ascii_letters, k=string_len)) for _ in range(num_calls)]
        print(f'Timing {num_calls} calls')
        time_taken = timer()
        for test_string in strings:
            lcps(test_string, 1, 1)
        time_taken = timer() - time_taken
        print('Time taken:', time_taken)
        print('Avg time taken:', time_taken / num_calls)

    elif op == '4':
        raise NotImplementedError
