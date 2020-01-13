import unittest
import timeit

import fdp_original
import fdp_optimized
from numpy import array_equal

# skip fdp_c tests if it's not already built
try:
    import fdp_c
except ImportError:
    FDP_C_UNAVAILABLE = True
else:
    FDP_C_UNAVAILABLE = False


class TestCorrectOutput (unittest.TestCase):

    GIVEN_SECRET = b'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'

    @classmethod
    def setUpClass(cls):
        state, echoes = fdp_original.encode(cls.GIVEN_SECRET)
        cls.expected_state = state
        cls.expected_echoes = echoes

    def perform_test(self, encode):
        state, echoes = encode(self.GIVEN_SECRET)
        self.assertEqual(state, self.expected_state)
        self.assertTrue(array_equal(echoes, self.expected_echoes))

    def test_optimized(self):
        self.perform_test(fdp_optimized.encode)

    @unittest.skipIf(FDP_C_UNAVAILABLE, "fdp_c is not built on this system")
    def test_c(self):
        self.perform_test(fdp_c.encode)


class TimeAlgorithms (unittest.TestCase):

    def time(self, name):
        REPETITIONS = 100
        setup = f"from {name} import encode; import secrets"
        statement = 'encode(secrets.token_bytes(40))'
        seconds = timeit.timeit(statement, setup=setup, number=REPETITIONS)
        seconds /= REPETITIONS
        msecs = seconds * 1000
        print(f'{name} time: {REPETITIONS} loops, average {msecs:.2f} msec')

    def test_time_original(self):
        self.time('fdp_original')

    def test_time_optimized(self):
        self.time('fdp_optimized')

    @unittest.skipIf(FDP_C_UNAVAILABLE, "fdp_c is not built on this system")
    def test_time_c(self):
        self.time('fdp_c')


if __name__ == '__main__':
    print("Running FilterDelayPermute tests (should take < 10 seconds)")
    print("Currently, this file:")
    print('\t', "* tests the correctness of fdp_optimized.encode")
    print('\t', '* tests the correctness of fdp_c.encode (if defined)')
    print('\t', "* times fdp_original, fdp_optimized, and fdp_c (if defined)")
    print()
    unittest.main()
