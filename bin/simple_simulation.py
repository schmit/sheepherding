from sheepherding.world.world import World
from sheepherding.viz.draw import draw_world
from sheepherding.ai.ai import GoTargetAI
from sheepherding.ai.learning import QLearner
from sheepherding.ai.features import TargetFeature
from sheepherding.util import running_avg

import time

import nodebox.graphics as ng
import matplotlib.pyplot as plt

# define world
width = 500
height = 500
speed = 0.2


# define AI for dogs, in this case, they share the same AI with a QLearner
def actions(state):
    result = ['left', 'right', 'none']
    if state.own_speed > 0:
        result.append('slower')
    if state.own_speed < 5:
        result.append('faster')
    return result

discount = 0.95
exploration_prob = 0.2
learner = QLearner(actions, discount, TargetFeature(), exploration_prob)
dog_ai = GoTargetAI(learner)

total_rewards = []

nsim = 100

print 'Running simulation...',
start_time = time.time()
for _ in xrange(nsim):
    # create world
    world = World(width, height, speed=speed)
    world.populate_sheep(1)
    world.populate_dogs(1, dog_ai)

    world.run(20)

    total_reward = sum(sum(dog.ai.rewards) for dog in world.dogs)
    total_rewards.append(total_reward)

print 'done in {:0.2f} seconds'.format(time.time() - start_time)

print 'Weights:'
print world.dogs[0].ai.rl.weights

print 'Showing simulation...',
draw_world(world)
print 'done'

print total_rewards
plt.plot(total_rewards)
plt.show()

