from animal import Animal

import nodebox.graphics as ng

class Dog(Animal):
    def __init__(self, world, loc, ai):
        Animal.__init__(self, world, loc)
        self.speed = 5.0
        self.ai = ai

    def update(self):
        angle_to_target = self.loc.angle(self.world.target)
        self.loc = self.loc.move(self.world.speed * self.speed, angle_to_target+1.5)

    def draw(self):
        radius = 5
        clr = ng.Color(0.1, 0.1, 0.1, 0.9)
        ng.ellipse(self.loc.x, self.loc.y,
           radius, radius,
           draw=True, fill=clr)
