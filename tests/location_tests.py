from nose.tools import *
from  sheepherding.world.location import *

from math import pi

class TestLocation:

    def setup(self):
        self.a = Location(0, 0)
        self.b = Location(3, 0)
        self.c = Location(2, 2)

    def teardown(self):
        pass

    def test_location_distance(self):
        assert_almost_equal(self.a.distance(self.b), 3)
        assert_almost_equal(self.c.distance(self.a), 2.82842712475)

    def test_location_angle(self):
        assert_almost_equal(self.a.angle(self.b), 0)
        assert_almost_equal(self.b.angle(self.a), pi)
        assert_almost_equal(self.a.angle(self.c), pi / 4)

    def test_move(self):
        d = self.a.move(1, 0)
        assert_almost_equal(d.x, 1)
        assert_almost_equal(d.y, 0)

        e = self.a.move(1, 4*pi)
        assert_almost_equal(e.x, 1)
        assert_almost_equal(e.y, 0)

        f = self.a.move(1, pi/2)
        assert_almost_equal(f.x, 0)
        assert_almost_equal(f.y, 1)

        g = self.b.move(3, pi/2)
        assert_almost_equal(g.x, 3)
        assert_almost_equal(g.y, 3)


