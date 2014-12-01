from sheepherding.ai.simulator import Simulator
from sheepherding.util import running_avg
from sheepherding.viz.draw import draw_world

import sheepherding.ai.features as features

import matplotlib.pyplot as plt
import seaborn

import sys

simulator = Simulator(n_dogs=1, n_sheep=1, objective='herdsheep', model='linear', feature_extractor=features.SheepFeature(),
    world_width=300, world_height=300)

# start with exploring a lot
simulator.run(int(sys.argv[1]))

draw_world(simulator.world)

simulator.print_weights()

print sum(simulator.rewards)

plt.plot(running_avg(simulator.rewards))
plt.savefig('rewards.pdf')

