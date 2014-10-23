from sheepherding.world.world import World
from sheepherding.viz.draw import draw_world
from sheepherding.ai.ai import GoTargetAI
from sheepherding.ai.learning import QLearner
from sheepherding.ai.features import TargetFeature

import time

import nodebox.graphics as ng

# define world
width = 500
height = 500
speed = 1.0

# create world
world = World(width, height, speed=speed)

# define AI for dogs, in this case, they share the same AI with a QLearner
def actions(state):
    result = ['left', 'right']
    if state.own_speed > 0:
        result.append('slower')
    if state.own_speed < 5:
        result.append('faster')
    return result

discount = 0.95
exploration_prob = 0.2
learner = QLearner(actions, discount, TargetFeature(), exploration_prob)
dog_ai = GoTargetAI(learner)


world.populate_sheep(1)
world.populate_dogs(1, dog_ai)

print 'Running simulation...',
start_time = time.time()
world.run(3)
print 'done in {:0.2f} seconds'.format(time.time() - start_time)

total_rewards = sum(sum(dog.ai.rewards) for dog in world.dogs)

print 'Total rewards: {}'.format(total_rewards)

print 'Showing simulation...',
draw_world(world)
print 'done'