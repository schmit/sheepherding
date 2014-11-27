from animal import Animal
from ..ai.state import State
from location import Location

from math import pi
import random

import nodebox.graphics as ng

class Dog(Animal):
    def __init__(self, world):
        Animal.__init__(self, world)
        self.speed = 3.0
        self.angle = 0.0

    def reset(self):
        self.loc = self.random_location()

    def random_location(self):
        x, y = random.choice((self.world.border, self.world.width-self.world.border)), random.choice((self.world.border, self.world.height-self.world.border))
        return Location(x, y)

    # Get move from AI
    def getMove(self):
        state = State(self)
        self.action = self.world.ai.getAction(state)
        if self.action == 'towards':
            self.angle = state.min_sheep_a
        elif self.action == 'away':
            self.angle = state.min_sheep_a + pi
        elif self.action == 'left':
            self.angle = state.min_sheep_a + 0.2 * pi
        elif self.action == 'right':
            self.angle = state.min_sheep_a - 0.2 * pi

        # save for evaluate()
        self.old_state = state

    # Evaluate
    def evaluate(self):
        self.new_state = State(self)
        self.world.ai.evaluate(self.old_state, self.action, self.new_state)

    # An update is moving at certain speed in certain direction
    def update(self):
        self.loc = self.loc.move(self.world.speed * self.speed, self.angle)
        self.save_history()


