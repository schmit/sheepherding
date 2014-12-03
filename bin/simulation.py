from sheepherding.ai.simulator import Simulator
from sheepherding.util import runningAvg
from sheepherding.viz.draw import drawWorld

import sheepherding.ai.features as features

import matplotlib.pyplot as plt
import seaborn

import sys

simulator = Simulator(n_dogs=1, n_sheep=1, objective='herdsheep', model='linear', feature_extractor=features.SheepFeature(),
    world_width=400, world_height=400)

# start with exploring a lot
simulator.run(int(sys.argv[1]))

drawWorld(simulator.world)

simulator.printWeights()

print sum(simulator.rewards)

plt.plot(runningAvg(simulator.rewards))
plt.savefig('rewards.pdf')

