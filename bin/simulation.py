from sheepherding.ai.simulator import Simulator
from sheepherding.util import runningAvg
from sheepherding.viz.draw import drawWorld

import sheepherding.ai.features as features

import matplotlib.pyplot as plt
import seaborn

import sys

try:
    RUNS = int(sys.argv[1])
    NSHEEP = int(sys.argv[2])
    MODEL = sys.argv[3]
    assert MODEL in ['linear', 'baseline']
except:
    print 'ERROR: Parsing input'
    print 'Usage: python simulation.py RUNS NSHEEP MODEL'
    print 'where RUNS and NSHEEP are ints, and model is linear or baseline'
    raise

simulator = Simulator(n_dogs=3, n_sheep=NSHEEP, objective='herdsheep', model=MODEL, feature_extractor=features.SheepFeature(),
    world_width=300, world_height=300)

simulator.run(RUNS)

drawWorld(simulator.world)

simulator.printWeights()

print sum(simulator.rewards)

plt.plot(runningAvg(simulator.rewards))
plt.xlabel('iteration')
plt.ylabel('running average of reward')
plt.title('Q-learning convergence, {} sheep'.format(NSHEEP))
plt.savefig('rewards{}.pdf'.format(NSHEEP))

