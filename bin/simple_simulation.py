from sheepherding.world.world import World
from sheepherding.simulation.draw import draw_world

import time

import nodebox.graphics as ng

width = 500
height = 500
world = World(width, height)
world.populate_sheep(30)
world.populate_dogs(3)

print 'Running simulation...',
start_time = time.time()
world.run(3)
print 'done in {:0.2f} seconds'.format(time.time() - start_time)

print 'Showing simulation...',
draw_world(world)
print 'done'