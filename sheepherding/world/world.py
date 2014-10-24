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
        self.set_target()


    def populate_sheep(self, n_sheep):
        ''' populate the world with n_sheep sheep '''
        # stay away from border
        border = 50

        for _ in xrange(n_sheep):
            loc = Location(random.randint(border, self.width-border),
                    random.randint(border, self.height-border))
            self.add_sheep(loc)

    def add_dog(self, ai):
        ''' add a specific dog to the world at random location '''
        # reset ai
        ai.reset()
        # give random location to dog: one of the corners
        border = 50
        x = random.choice((border, self.width-border))
        y = random.choice((border, self.height-border))
        loc = Location(x, y)
        dog = Dog(self, ai, loc)
        self.dogs.append(dog)

    def add_sheep(self, loc):
        self.sheeps.append(Sheep(self, loc))

    def set_target(self, target_border=100, target_radius=40):
        self.target = Location(random.randint(target_border, self.width - target_border), random.randint(target_border, self.height - target_border))
        # radius
        self.target_radius = target_radius

    def update(self):
        # first find moves for every dog, every 10th iteration
        if self.iteration % 10 == 0:
            for dog in self.dogs:
                dog.getMove()

        # update the world
        for sheep in self.sheeps:
            sheep.update()
        for dog in self.dogs:
            dog.update()

        # evaluate moves by dogs just before new iteration
        if self.iteration % 10 == 9:
            for dog in self.dogs:
                dog.evaluate()

        self.iteration += 1

    def run(self, seconds):
        ''' run world for a number of seconds '''
        for _ in xrange(30*seconds):
            self.update()
