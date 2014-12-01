''' simple script to test State and Features '''

from sheepherding.ai.state import State
import sheepherding.ai.features as feature
from sheepherding.world.world import World
from sheepherding.world.sheep import Sheep
from sheepherding.world.dog import Dog
from sheepherding.world.location import Location


import sys

world = World(500, 500)

# target at 100, 100
world.target = Location(0, 0)


sheep = Sheep(world)
dog = Dog(world)

dogx = float(sys.argv[1])
dogy = float(sys.argv[2])
sheepx = float(sys.argv[3])
sheepy = float(sys.argv[4])

dog.loc = Location(dogx, dogy)
sheep.loc = Location(sheepx, sheepy)

world.dogs.append(dog)
world.sheeps.append(sheep)

state = world.dogs[0].getState()
f = feature.SheepFeature()


state.details()

print f(state, 'left')