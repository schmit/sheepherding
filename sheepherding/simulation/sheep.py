from animal import Animal

import random
from math import cos, sin, atan2, pi

import nodebox.graphics as ng


class Sheep(Animal):
    def __init__(self, world, loc):
        Animal.__init__(self, world, loc)
        self.force_angle = (random.random()*2-1) * pi

    def compute_force(self):
        ''' compute the force on the sheep '''
        def sheep_force(distance):
            # the further away, the less the attractive force
            # note attraction is negative
            alpha = 1.0
            x = alpha * distance
            attraction = 1 / (x+0.1)**0.3 - 0.3
            repulsion = 10 / (x+0.1)**2
            total = max(0, min(4, repulsion)) - max(0, min(1, attraction))
            return total

        def dog_force(distance):
            # the closer the dog, the stronger the force
            alpha = 1.0
            x = alpha * distance
            force = 10.0 / (x + 0.1) - 0.25 * x + 8
            return min(10, max(0, force))

        fx, fy = 0, 0
        for sheep in self.world.sheeps:
            if sheep is not self:
                distance, angle = self.loc.da(sheep.loc)
                total_force = sheep_force(distance)
                fx += total_force * cos(angle)
                fy += total_force * sin(angle)

        for dog in self.world.dogs:
            distance, angle = self.loc.da(dog.loc)
            total_force = dog_force(distance)
            fx += total_force * cos(angle)
            fy += total_force * sin(angle)

        self.force_magnitude = (fx**2 + fy**2)**0.5
        # new angle is influenced by previous: this provides more fluent movement
        self.force_angle = 0.5 * (atan2(fy, fx) - pi) + 0.5 * self.force_angle

    def compute_speed(self):
        hi_speed_th = 1.2
        if self.force_magnitude > hi_speed_th:
            self.speed = 2.5
        else:
            self.speed = 1.0

    def update(self):
        # compute all forces
        self.compute_force()
        self.compute_speed()

        # move according to forces
        self.loc = self.loc.move(self.world.speed * self.speed, self.force_angle)

    def draw(self):
        radius = 5
        if self.speed > 2:
            clr = ng.Color(0.9, 0.1, 0.1, 0.5)
        else:
            clr = ng.Color(0.9, 0.9, 0.9, 0.5)
        ng.ellipse(self.loc.x, self.loc.y,
           radius, radius,
           draw=True, fill=clr)