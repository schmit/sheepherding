import collections, random

# From cs221.stanford
from math import sqrt

# Abstract class: an RLAlgorithm performs reinforcement learning.  All it needs
# to know is the set of available actions to take.  The simulator (see
# simulate()) will call getAction() to get an action, perform the action, and
# then provide feedback (via incorporateFeedback()) to the RL algorithm, so it can adjust
# its parameters.
class Learner:
    # Your algorithm will be asked to produce an action given a state.
    def getAction(self, state):
        raise NotImplementedError("Override me")

    # We will call this function when simulating an MDP, and you should update
    # parameters.
    # If |state| is a terminal state, this function will be called with (s, a,
    # 0, None). When this function is called, it indicates that taking action
    # |action| in state |state| resulted in reward |reward| and a transition to state
    # |newState|.
    def incorporateFeedback(self, state, action, reward, newState):
        raise NotImplementedError("Override me")


class QLearner(Learner):
    def __init__(self, actions, discount, feature_extractor, exploration_prob=0.2):
        self.actions = actions
        self.discount = discount
        self.feature_extractor = feature_extractor
        self.exploration_prob = exploration_prob
        self.weights = collections.Counter()
        self.numIters = 0

    # Return the Q function associated with the weights and features
    def getQ(self, state, action):
        score = 0
        for f, v in self.feature_extractor(state, action):
            score += self.weights[f] * v
        return score

    # This algorithm will produce an action given a state.
    # Here we use the epsilon-greedy algorithm: with probability
    # |exploration_prob|, take a random action.
    def getAction(self, state):
        self.numIters += 1
        if random.random() < self.exploration_prob:
            return random.choice(self.actions(state))
        else:
            return max((self.getQ(state, action), action) for action in self.actions(state))[1]

    # Call this function to get the step size to update the weights.
    def getStepSize(self):
        return 1.0 / sqrt(self.numIters)

    # We will call this function with (s, a, r, s'), which you should use to update |weights|.
    # Note that if s is a terminal state, then s' will be None.  Remember to check for this.
    # You should update the weights using self.getStepSize(); use
    # self.getQ() to compute the current estimate of the parameters.
    def incorporateFeedback(self, state, action, reward, newState):
        # compute residual
        if newState is None:
            residual = reward -  self.getQ(state, action)
        else:
            residual = reward + self.discount * max(self.getQ(newState, newAction) for newAction in self.actions(newState)) - self.getQ(state, action)

        # update weights
        phi = self.feature_extractor(state, action)
        for featureKey, featureValue in phi:
            self.weights[featureKey] += self.getStepSize() * residual * featureValue
