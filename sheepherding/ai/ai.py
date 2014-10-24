from ..world.location import Location
from learning import QLearner

class AI:
    def __init__(self, learner):
        self.learner = learner
        self.rewards = []
        self.actions = []

    def setLearner(self, learner):
        self.learner = learner

    def getAction(self, state):
        action = self.learner.getAction(state)
        # save action and state for evaluation step
        self.action = action
        self.actions.append(action)
        self.oldState = state
        return action

    def evaluate(self, newState):
        reward = self.computeReward(self.oldState, self.action, newState)
        self.rewards.append(reward)
        self.learner.incorporateFeedback(self.oldState, self.action, reward, newState)

    def computeReward(self, state, action, newState):
        return 0.0

    def reset(self):
        ''' resets rewards and actions '''
        self.rewards = []
        self.actions = []


class GoTargetAI(AI):
    '''
    The GoTargetAI implements the simple task of moving the dog itself to a target.
    '''
    def computeReward(self, state, action, newState):
        '''
        Return the reciprocal of distance to target
        '''
        # convert to location so we can use distance function
        own_location = Location(newState.own_location[0], newState.own_location[1])
        distance_target = own_location.distance(newState.target_location)
        if distance_target < newState.target_radius:
            return 1.0
        return -0.1
