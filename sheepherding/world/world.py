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
        self.rewards = []

        # dogs and sheep are stored in lists
        self.sheeps = []
        self.dogs = []

        # target
        self.setTarget()

    def populateSheep(self, n_sheep):
        ''' populate the world with n_sheep sheep '''
        for _ in xrange(n_sheep):
            self.addSheep()

    def populateDogs(self, n_dogs):
        for _ in xrange(n_dogs):
            self.addDog()

    def addDog(self):
        ''' add a specific dog to the world at random location '''
        self.dogs.append(Dog(self))

    def addSheep(self):
        self.sheeps.append(Sheep(self))

    def setTarget(self, target_border=50, target_radius=25):
        try:
            self.target = Location(random.randint(target_border, self.width - target_border), random.randint(target_border, self.height - target_border))
        except:
            self.target = Location(self.width/2, self.height/2)
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
        reward = 0
        while iteration < 30 * seconds:
            # update world
            self.update()

            # check whether we are done
            if self.ai.done: break
            iteration += 1

        self.reset()

    def randomLocation(self):
        x, y = random.randint(self.border, self.width-self.border), random.randint(self.border, self.width-self.border)
        return Location(x, y)
