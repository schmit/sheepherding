from sheepherding.simulation.world import World

import nodebox.graphics as ng

width = 500
height = 500

world = World(width, height)
world.populate_sheep(30)
world.populate_dogs(3)

ng.canvas.fps = 30
ng.canvas.size = width, height
ng.canvas.run(world.draw(ng.canvas))