from sheepherding.ai.simulator import Simulator
from sheepherding.util import running_avg
from sheepherding.viz.draw import draw_world

import matplotlib.pyplot as plt
import seaborn

simulator = Simulator(n_sheep=0)
simulator.init_dog_ai(1)
rewards = simulator.run(30, save_worlds=10)

simulator.print_weights()

draw_world(simulator.worlds[-1])

plt.plot(running_avg(rewards))
plt.show()
