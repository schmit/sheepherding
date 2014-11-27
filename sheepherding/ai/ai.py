from ..world.location import Location
from learning import QLearner


class AI:
    def __init__(self, learner):
        self.learner = learner
        self.rewards = []
        self.actions = []
        self.done = False

    def setLearner(self, learner):
        self.learner = learner

    def getAction(self, state):
        return self.learner.getAction(state)

    def evaluate(self, old_state, action, new_state):
        reward = self.computeReward(old_state, action, new_state)
        self.rewards.append(reward)
        self.learner.incorporateFeedback(old_state, action, reward, new_state)

    def computeReward(self, state, action, new_state):
        return 0.0

    def reset(self):
        ''' resets rewards and actions '''
        total_reward = sum(self.rewards)
        self.rewards = []
        self.actions = []
        self.done = False
        return total_reward


class GoTargetAI(AI):
    '''
    The GoTargetAI implements the simple task of moving the dog itself to a target.
    '''
    def computeReward(self, state, action, new_state):
        '''
        Return 1 if dog is at target
        '''
        # convert to location so we can use distance function
        own_location = Location(new_state.own_location[0], new_state.own_location[1])
        distance_target = own_location.distance(new_state.target_location)
        if distance_target < new_state.target_radius:
            self.done = True
            return 1.0
        return 0.0


class HerdSheepAI(AI):
    '''
    The HerdSheepAI implements the task of moving sheep to the target.
    '''
    def computeReward(self, state, action, new_state):
        '''
        Return +1 for each sheep in target location
        '''
        # convert to location so we can use distance function
        reward = 0
        for sheep in state.sheep_locations:
            distance_target = Location(sheep[0], sheep[1]).distance(new_state.target_location)
            if distance_target < new_state.target_radius:
                reward += 1

        # done if all sheep in target location
        if reward == len(state.sheep_locations):
            self.done = True

        return reward

