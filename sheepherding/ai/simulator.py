import sheepherding.ai.ai as ai
import sheepherding.ai.learning as learning
import sheepherding.ai.features as features
from sheepherding.ai.model import LinearModel, NeuralModel, StaticModel

from sheepherding.world.dog import Dog
from sheepherding.world.world import World

import time
import datetime
import sys


class Simulator:
    def __init__(self, n_sheep=0, model='linear', learner='qlearner',
                 feature_extractor = features.TargetFeature(),
                 world_width=500, world_height=500, world_speed=0.3):
        self.width = world_width
        self.height = world_height
        self.speed = world_speed
        self.n_sheep = n_sheep
        self.dog_ais = []

        # ai and learner defaults
        self.ai_obj = 'gotarget'

        self.model = model
        self.learner = learner
        self.learner_actions = self.get_actions()
        self.learner_discount = 0.95
        self.learner_feature_extractor = feature_extractor
        self.learner_exploration_prob = 0.2

        self.rewards = [0]

    def set_ai(self, obj):
        self.ai_obj = obj

    def get_ai(self, learner):
        if self.ai_obj == 'gotarget':
            return ai.GoTargetAI(learner)
        else: raise NotImplementedError('Unknown AI')

    def set_learner(self):
        ''' function to specify what learner to use '''
        # to do
        raise NotImplementedError('set_learner is not implemented yet')

    def get_learner(self):
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
                    self.learner_feature_extractor, self.learner_exploration_prob)
        else:
            raise NotImplementedError('learner: {} not implemented'.format(self.learner))

    def init_dog_ai(self, n_dogs, ai='gotarget', learner='qlearner'):
        for _ in xrange(n_dogs):
            learner = self.get_learner()
            ai = self.get_ai(learner)
            self.dog_ais.append(ai)

    def run(self, nsim, seconds=10):
        print 'Starting simulations:',
        start_time = time.time()
        world = World(self.width, self.height, speed=self.speed)
        world.populate_sheep(self.n_sheep)

        # add dog(s) to world
        for dog_ai in self.dog_ais:
            world.add_dog(dog_ai)

        for sim in xrange(nsim):
            reward = 0
            world.run(seconds)

            # compute reward
            for dog in world.dogs:
                reward += dog.reward

            self.rewards.append(reward)

            if sim % 100 == 0: print '.',

        self.dog_ais[0].learner.model.save()

        print 'done in {} seconds'.format(time.time() - start_time)
        return self.rewards, world

    def print_weights(self):
        for dogai in self.dog_ais:
            print dogai.learner.model

    def get_actions(self):
        '''
        helper function that returns function for actions of dog
        '''
        def dog_actions(state):
            return ['walk', 'left', 'right', 'run']
        return dog_actions

