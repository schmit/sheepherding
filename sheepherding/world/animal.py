from math import pi
import random

class Animal:
    def __init__(self, world, loc):
        self.speed = 1
        self.world = world
        self.loc = loc
        self.history = []

    def save_history(self):
        self.history.append((self.loc.x, self.loc.y))

    def update(self):
        ''' wander mindlessly '''
        angle = (random.random()*2-1)*pi
        self.loc = self.loc.update(self.world.speed * 1, angle)