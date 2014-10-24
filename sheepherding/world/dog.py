from animal import Animal
from ..ai.state import State
from location import Location

from math import pi

import nodebox.graphics as ng

class Dog(Animal):
    def __init__(self, world, ai, loc=Location(0, 0)):
        Animal.__init__(self, world, loc)
        self.speed = 3.0
        self.angle = 0.0

        self.action = 'nothing'
        self.ai = ai

        self.max_speed = 5.0
        self.actions = []

    # Actions for dog
    def run(self):
        ''' Move at speed of 5 '''
        self.speed = 5.0

    def stop(self):
        ''' Stop '''
        self.speed = 0.0

    def walk(self):
        ''' Move at speed of 1 '''
        self.speed = 1.0

    def left(self):
        ''' turn left such that full turn takes 1 second '''
        self.angle += pi / 5.0

    def right(self):
        ''' turn right such that full turn takes 1 second '''
        self.angle -= pi / 5.0


    # Get move from AI
    def getMove(self):
        self.action = self.ai.getAction(State(self))
        self.actions.append(self.action)
        if self.action == 'run':
            self.run()
        elif self.action == 'walk':
            self.walk()
        elif self.action == 'stop':
            self.stop()
        elif self.action == 'left':
            self.left()
        elif self.action == 'right':
            self.right()


    # Evaluate
    def evaluate(self):
        self.ai.evaluate(State(self))

    # An update is moving at certain speed in certain direction
    def update(self):
        self.loc = self.loc.move(self.world.speed * self.speed, self.angle)
        self.save_history()
