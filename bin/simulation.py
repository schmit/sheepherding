from sheepherding.ai.simulator import Simulator
from sheepherding.util import running_avg
from sheepherding.viz.draw import draw_world

import sheepherding.ai.features as features

import matplotlib.pyplot as plt
import seaborn

import sys

simulator = Simulator(n_sheep=1, model='linear', feature_extractor=features.TargetFeature(),
    world_width=200, world_height=200)
simulator.init_dog_ai(1)

# start with exploring a lot
rewards, world = simulator.run(int(sys.argv[1]))

draw_world(world)

simulator.print_weights()

plt.plot([x/(i+1) for i, x in enumerate(rewards)])
plt.show()
