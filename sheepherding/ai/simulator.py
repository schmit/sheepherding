import sheepherding.ai.ai as ai
import sheepherding.ai.learning as learning
import sheepherding.ai.features as features
from sheepherding.ai.model import LinearModel, NeuralModel, StaticModel

from sheepherding.world.dog import Dog
from sheepherding.world.world import World

import time
import datetime
import sys

try:
    import cPickle as pickle
except:
    import pickle


class Simulator:
    def __init__(self, n_dogs=1, n_sheep=1,
                objective='gotarget', model='linear', learner='qlearner',
                feature_extractor = features.TargetFeature(),
                world_width=500, world_height=500, world_speed=0.3,
                learner_discount = 0.95,
                learner_exploration_prob_max=0.1, learner_exploration_prob_min=0.03):
        self.width = world_width
        self.height = world_height
        self.speed = world_speed
        self.n_sheep = n_sheep
        self.n_dogs = n_dogs

        # ai and learner defaults
        self.ai_obj = objective
        self.model = model
        self.learner = learner
        self.learner_actions = self.getActions()
        self.learner_discount = learner_discount
        self.learner_feature_extractor = feature_extractor
        self.learner_exploration_prob_max = learner_exploration_prob_max
        self.learner_exploration_prob_min = learner_exploration_prob_min

        self.rewards = [0]

        self.setupWorld()

    def setupWorld(self):
        self.world = World(self.width, self.height, speed=self.speed)
        self.world.populateSheep(self.n_sheep)
        self.world.populateDogs(self.n_dogs)
        self.world.ai = self.getAi(self.getLearner())

    def getAi(self, learner):
        if self.ai_obj == 'gotarget':
            return ai.GoTargetAI(learner)
        elif self.ai_obj == 'herdsheep':
            return ai.HerdSheepAI(learner)
        else: raise NotImplementedError('Unknown AI')

    def setLearner(self):
        ''' function to specify what learner to use '''
        # to do
        raise NotImplementedError('set_learner is not implemented yet')

    def getLearner(self):
        if self.model == 'linear':
            model = LinearModel()
        elif self.model == 'neural':
            model = NeuralModel(7)
        elif self.model == 'baseline':
            model = StaticModel()
        else:
            raise NotImplementedError('model: {} not implemented'.format(self.model))

        if self.learner == 'qlearner':
            return learning.QLearner(model, self.learner_actions, self.learner_discount,
                    self.learner_feature_extractor, self.learner_exploration_prob_max)
        else:
            raise NotImplementedError('learner: {} not implemented'.format(self.learner))

    def run(self, nsim, seconds=15):
        print 'Starting simulations'
        start_time = time.time()

        print '================================================'
        print 'percentage | time taken | total time | time left'
        print '------------------------------------------------'
        for sim in xrange(nsim):
            self.world.run(seconds)

            # reset AI for next run
            reward = self.world.ai.reset()
            self.rewards.append(reward)

            if (sim+1) % (nsim/17) == 0:
                self.printProgress(sim+1, nsim, start_time)
                self.updateExplorationProb(sim+1, nsim)

        self.world.ai.learner.model.save()
        self.saveRewards()

        print 'done in {} seconds'.format(time.time() - start_time)

    def printWeights(self):
        print self.world.ai.learner.model

    def printProgress(self, sim, nsim, start_time):
        frac_done = float(sim)/nsim
        time_taken = time.time() - start_time
        total_time = time_taken / frac_done
        time_to_go = total_time * (1-frac_done)
        print '{:6.0f}%  {:10.0f}s {:10.0f}s {:10.0f}s'.format(frac_done*100, time_taken, total_time, time_to_go)
        sys.stdout.flush()

    def getActions(self):
        '''
        helper function that returns function for actions of dog
        '''
        def dog_actions(state):
            return ['towards', 'away', 'left', 'right']
        return dog_actions

    def saveRewards(self):
        with open('rewards_{}.pkl'.format(self.model), 'w') as f:
            pickle.dump(self.rewards, f)

    def updateExplorationProb(self, sim, nsim):
        frac_done = float(sim) / nsim
        # allows for nonlinear changes
        power = 0.25
        self.world.ai.learner.exploration_prob = frac_done**power * self.learner_exploration_prob_min + (1-frac_done**power) * self.learner_exploration_prob_max

