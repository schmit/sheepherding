from sheep import Sheep
from dog import Dog
from location import Location

import random

import nodebox.graphics as ng

class World:
    '''
    World implements the structure of the simulation.
    It includes the sheep and dogs, the driver that draws the world etc.
    '''
    def __init__(self, width, height, speed=1.0):
        self.width = width
        self.height = height
        self.speed = speed
        self.iteration = 0
        self.reward = 0

        # dogs and sheep are stored in lists
        self.sheeps = []
        self.dogs = []

        # TARGET
        # location
        self.target = Location(self.width/2 + random.randint(-50, 50),
                self.height/2 + random.randint(-50, 50))
        # radius
        self.target_radius = 20

    def populate_sheep(self, n_sheep):
        border = 100

        for _ in xrange(n_sheep):
            loc = Location(random.randint(border, self.width-border),
                    random.randint(border, self.height-border))
            self.add_sheep(loc)

    def populate_dogs(self, n_dogs, ai=None):
        border = 100
        for _ in xrange(n_dogs):
            loc = Location(random.randint(border, self.width-border),
                    random.randint(border, self.height-border))
            self.add_dog(loc, ai)

    def add_dog(self, loc, ai):
        self.dogs.append(Dog(self, loc, ai))

    def add_sheep(self, loc):
        self.sheeps.append(Sheep(self, loc))

    def update(self):
        # first find moves for every dog
        for dog in self.dogs:
            dog.getMove()

        # update the world
        for sheep in self.sheeps:
            sheep.update()
        for dog in self.dogs:
            dog.update()

        # evaluate moves by dogs
        for dog in self.dogs:
            dog.evaluate()

        self.iteration += 1

    def run(self, seconds):
        ''' run world for a number of seconds '''
        for _ in xrange(30*seconds):
            self.update()
