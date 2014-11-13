from sheepherding.ai.simulator import Simulator
from sheepherding.util import running_avg
from sheepherding.viz.draw import draw_world

import sheepherding.ai.features as features

import matplotlib.pyplot as plt
import seaborn

import sys

simulator = Simulator(n_sheep=1, model='neural', feature_extractor=features.TargetFeature(),
    world_width=200, world_height=200)
simulator.init_dog_ai(1)

# start with exploring a lot
simulator.learner_exploration_prob = 0.5
rewards = simulator.run(int(sys.argv[1])/2, save_worlds=999)

# then exploit more
simulator.learner_exploration_prob = 0.2
rewards = simulator.run(int(sys.argv[1])/2, save_worlds=999)
# simulator.save_worlds()

draw_world(simulator.worlds[-1])

simulator.print_weights()

plt.plot(running_avg(rewards))
plt.show()
