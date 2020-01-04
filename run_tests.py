import unittest
import timeit

import fdp_original
import fdp_numpy
import fdp_verbose
from numpy import array_equal

class TestCorrectOutput (unittest.TestCase):

    GIVEN_SECRET = b'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'

    @classmethod
    def setUpClass (cls):
        state, echoes = fdp_original.encode(cls.GIVEN_SECRET)
        cls.expected_state = state
        cls.expected_echoes = echoes

    def perform_test (self, encode):
        state, echoes = encode(self.GIVEN_SECRET)
        self.assertEqual(state, self.expected_state)
        self.assertTrue(array_equal(echoes, self.expected_echoes))

    def test_numpy (self):
        self.perform_test(fdp_numpy.encode)

    def test_verbose (self):
        self.perform_test(fdp_verbose.encode)


class TimeAlgorithms (unittest.TestCase):

    def time (self, name):
        REPETITIONS = 100
        setup = f'from {name} import encode; import secrets'
        statement = 'encode(secrets.token_bytes(40))'
        seconds = timeit.timeit(statement, setup=setup, number=REPETITIONS)
        seconds /= REPETITIONS
        milliseconds = seconds * 1000
        print(f'{name} time: {REPETITIONS} loops, average {milliseconds:.2f} msec')

    def test_time_original (self):
        self.time('fdp_original')

    def test_time_numpy (self):
        self.time('fdp_numpy')

    def test_time_verbose (self):
        self.time('fdp_verbose')

if __name__ == '__main__':
    unittest.main()
