from nose.tools import *
from  sheepherding.util import *

from math import pi

class TestUtil:

    def test_sign(self):
        pairs = [(4.0, 1), (4, 1), (0, 0), (-5.3, -1)]
        for x, y in pairs:
            assert_equal(sign(x), y)

    def test_running_avg(self):
        pairs = [([0], [0]), ([1, 2, 4], [1, 1.5, 7.0/3.0])]
        for x, y in pairs:
            assert_equal(running_avg(x), y)


    def test_angle_diff(self):
        # known values of current, aim with solution:
        known = [((0, pi/2), pi/2),
                 ((0.3*pi, 0.4*pi), 0.1*pi),
                 ((-0.3*pi, 0.4*pi), 0.7*pi),
                 ((0.4*pi, 0.3*pi), -0.1*pi),
                 ((0.9*pi, -0.9*pi), 0.2*pi),
                 ((-0.9*pi, 0.9*pi), -0.2*pi)]
        for (current, aim), answer in known:
            print current, aim, answer
            assert_equal(angle_difference(current, aim), answer)