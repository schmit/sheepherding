from collections import Counter
try:
    import cPickle as pickle
except:
    import pickle

class Model:
    def save(self, filen=None):
        if filen == None:
            filen = self.__class__.__name__
        with open('{}.pkl'.format(filen), 'w') as f:
            pickle.dump(self.weights, f)

    def load(self, filen=None):
        if filen == None:
            filen = self.__class__.__name__
        with open('{}.pkl'.format(filen), 'r') as f:
            self.weights = pickle.load(f)

class LinearModel(Model):
    def __init__(self):
        self.weights = Counter()

    def eval(self, features):
        score = 0
        for feature, value in features:
            score += self.weights[feature] * value
        return score

    def update(self, features, residual, stepsize):
        for feature, value in features:
            self.weights[feature] += stepsize * residual * value

    def __repr__(self):
        return '\n'.join(['{:30s} {:3.3f}'.format(k, v) for k, v in self.weights.iteritems()])

