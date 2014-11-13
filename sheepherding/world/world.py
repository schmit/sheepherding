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
        # don't initialize in border
        self.border = 20

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
        for _ in xrange(n_sheep):
            self.add_sheep()

    def add_dog(self, ai):
        ''' add a specific dog to the world at random location '''
        # reset ai
        ai.reset()
        # give random location to dog: one of the corners
        dog = Dog(self, ai)
        self.dogs.append(dog)

    def add_sheep(self):
        self.sheeps.append(Sheep(self))

    def set_target(self, target_border=50, target_radius=25):
        self.target = Location(random.randint(target_border, self.width - target_border), random.randint(target_border, self.height - target_border))
        # radius
        self.target_radius = target_radius

    def reset(self):
        ''' random location for animals '''
        for sheep in self.sheeps:
            sheep.reset()

        for dog in self.dogs:
            dog.reset()

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
        iteration = 0
        while iteration < 30 * seconds:
            # update world
            self.update()

            # check whether we are done
            for dog in self.dogs:
                if dog.ai.done:
                    self.reset()

            iteration += 1

        self.reset()

    def random_location(self):
        x, y = random.randint(self.border, self.width-self.border), random.randint(self.border, self.width-self.border)
        return Location(x, y)
