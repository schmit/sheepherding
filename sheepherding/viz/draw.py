import nodebox.graphics as ng

class Draw:
    def __init__(self, world):
        self.world = world
        self.iteration = 0

    def draw(self, canvas):
        def d(canvas):
            canvas.clear()
            clr = ng.Color(0.09, 0.29, 0.1)
            ng.background(clr)
            ng.nostroke()

            # draw target
            clr = ng.Color(1.0, 1.0, 1.0, 0.1)
            ng.ellipse(self.world.target.x, self.world.target.y,
                    self.world.target_radius*2, self.world.target_radius*2,
                    draw=True, fill=clr)

            # draw sheep
            for sheep in self.world.sheeps:
                x, y = sheep.history[self.iteration]
                clr = ng.Color(0.9, 0.9, 0.9, 0.5)
                r = 4
                ng.ellipse(x, y, r, r, draw=True, fill=clr)

            # draw dogs
            for dog in self.world.dogs:
                x, y = dog.history[self.iteration]
                r = 4
                clr = ng.Color(0.1, 0.1, 0.1, 0.9)
                ng.ellipse(x, y, r, r, draw=True, fill=clr)

            # label = ng.Text('time: {}'.format(self.iteration / 30))
            # ng.text(label, 10, 10)
            # label = ng.Text('reward: {}'.format(self.world.rewards[self.iteration]))
            # ng.text(label, 10, 10)

            self.iteration = min(self.iteration + 1, self.world.iteration - 1)

        return d

def draw_world(world):
    ng.canvas.fps = 30
    ng.canvas.size = world.width, world.height
    draw = Draw(world)
    ng.canvas.run(draw.draw(ng.canvas))