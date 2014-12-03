from math import pi
import random

class Animal:
    def __init__(self, world):
        self.speed = 1
        self.world = world
        self.history = []

        # assign random location
        self.reset()

    def saveHistory(self):
        if len(self.history) < 1e6:
            self.history.append((self.loc.x, self.loc.y))

    def update(self):
        ''' wander mindlessly '''
        angle = (random.random()*2-1)*pi
        self.loc = self.loc.update(self.world.speed * 1, angle)

    # reset to random location
    def reset(self):
        self.loc = self.world.randomLocation()