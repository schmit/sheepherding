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
    def __init__(self, width, height, speed=0.2):
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
        self.targetradius = 20

        # REWARD

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

    def compute_reward(self):
        for sheep in self.sheeps:
            distance_to_target = sheep.loc.distance(self.target)
            if distance_to_target <= self.targetradius/2:
                self.reward += 1

    def update(self):
        for dog in self.dogs:
            dog.update()

        for sheep in self.sheeps:
            sheep.update()

        self.compute_reward()

        self.iteration += 1

    def draw(self, canvas):
        def d(canvas):
            canvas.clear()
            clr = ng.Color(0.09, 0.29, 0.1)
            ng.background(clr)
            ng.nostroke()

            # draw time and reward info
            label = ng.Text('time: {}\treward: {}'.format(self.iteration / 30, self.reward / 30))
            ng.text(label, 10, 10)

            # draw dogs
            for dog in self.dogs:
                dog.draw()

            # draw sheep
            for sheep in self.sheeps:
                sheep.draw()

            # draw target
            clr = ng.Color(1.0, 1.0, 1.0, 0.1)
            ng.ellipse(self.target.x, self.target.y,
                    self.targetradius, self.targetradius,
                    draw=True, fill=clr)
            clr = ng.Color(0.9, 0.9, 0.9, 0.9)

            self.update()

        return d
