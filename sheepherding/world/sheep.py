from animal import Animal

import random
from math import cos, sin, atan2, pi

import nodebox.graphics as ng


class Sheep(Animal):
    def __init__(self, world):
        Animal.__init__(self, world)
        self.force_angle = (random.random()*2-1) * pi

    def computeForce(self):
        ''' compute the force on the sheep '''
        def forceFunc(x, a=1.0, b=1.0):
            '''
            force function:
            x: input
            a: max distance of force
            b: force at distance 0
            '''
            f = b * (1.0 - (x / a)**0.5)
            return max(0, f)

        def sheepForce(distance):
            # the further away, the less the attractive force
            # note attraction is negative
            attraction = forceFunc(distance, 40.0, 1.0)
            repulsion = forceFunc(distance, 5.0, 4.0)
            total = repulsion - attraction
            return repulsion - attraction

        def dogForce(distance):
            # the closer the dog, the stronger the force
            return forceFunc(distance, 50.0, 25.0)

        fx, fy = 0, 0

        for sheep in self.world.sheeps:
            if sheep is not self:
                distance, angle = self.loc.da(sheep.loc)
                total_force = sheepForce(distance)
                fx += total_force * cos(angle)
                fy += total_force * sin(angle)

        for dog in self.world.dogs:
            distance, angle = self.loc.da(dog.loc)
            total_force = dogForce(distance)
            fx += total_force * cos(angle)
            fy += total_force * sin(angle)

        self.force_magnitude = (fx**2 + fy**2)**0.5
        # new angle is influenced by previous: this provides more fluent movement
        self.force_angle = (atan2(fy, fx) - pi)

    def computeSpeed(self):
        hi_speed_th = 10.0
        if self.force_magnitude > hi_speed_th:
            self.speed = 4.0
        else:
            self.speed = min(self.force_magnitude, 1.0)

    def update(self):
        # compute all forces
        self.computeForce()
        self.computeSpeed()

        # move according to forces
        self.loc = self.loc.move(self.world.speed * self.speed, self.force_angle)
        self.saveHistory()
