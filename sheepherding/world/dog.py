from animal import Animal

from math import pi

import nodebox.graphics as ng

class Dog(Animal):
    def __init__(self, world, loc, ai):
        Animal.__init__(self, world, loc)
        self.speed = 3.0
        self.angle = 0.0
        self.ai = ai

        self.max_speed = 5.0

    # Actions for dog
    def speed_up(self):
        ''' increase speed by 1 up to max_speed '''
        self.speed = min(self.max_speed, self.speed + 1.0)

    def turn_left(self):
        ''' turn left such that full turn takes 1 second '''
        self.angle += 2*pi / 30.0

    def turn_right(self):
        ''' turn right such that full turn takes 1 second '''
        self.angle -= 2*pi / 30.0

    def slow_down(self):
        ''' slow down by 1 up to stopping '''
        self.speed = max(0, self.speed - 1.0)

    def update(self):
        self.loc = self.loc.move(self.world.speed * self.speed, self.angle)
        self.save_history()
