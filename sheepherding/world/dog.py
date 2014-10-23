from animal import Animal
from ..ai.state import State

from math import pi

import nodebox.graphics as ng

class Dog(Animal):
    def __init__(self, world, loc, ai):
        Animal.__init__(self, world, loc)
        self.speed = 3.0
        self.angle = 0.0

        self.action = 'nothing'
        self.ai = ai

        self.max_speed = 5.0
        self.actions = []

    # Actions for dog
    def faster(self):
        ''' increase speed by 1 up to max_speed '''
        self.speed = min(self.max_speed, self.speed + 0.3)

    def left(self):
        ''' turn left such that full turn takes 1 second '''
        self.angle += 2*pi / 10.0

    def right(self):
        ''' turn right such that full turn takes 1 second '''
        self.angle -= 2*pi / 10.0

    def slower(self):
        ''' slow down by 1 up to stopping '''
        self.speed = max(0, self.speed - 0.3)

    # Get move from AI
    def getMove(self):
        self.action = self.ai.getAction(State(self))
        self.actions.append(self.action)
        if self.action == 'faster':
            self.faster()
        elif self.action == 'left':
            self.left()
        elif self.action == 'right':
            self.right()
        elif self.action == 'slower':
            self.slower()

    # Evaluate
    def evaluate(self):
        self.ai.evaluate(State(self))

    # An update is moving at certain speed in certain direction
    def update(self):
        self.loc = self.loc.move(self.world.speed * self.speed, self.angle)
        self.save_history()
