from collections import Counter
try:
    import cPickle as pickle
except:
    import pickle

from neural import rectifier_network

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
    ''' Use a linear model for Q-learning '''
    def __init__(self, regularization=0.00001):
        try:
            self.load()
            print 'Loading trained model'
        except IOError:
            print 'Cant load trained model, using new model'
            self.weights = Counter()

        self.reg = regularization

    def eval(self, features):
        score = 0
        for feature, value in features:
            score += self.weights[feature] * value
        return score

    def update(self, features, residual, stepsize):
        for feature, value in features:
            self.weights[feature] += stepsize * (residual * value - self.reg * self.weights[feature])

    def __repr__(self):
        return '\n'.join(['{:30s} {:3.3f}'.format(k, v) for k, v in sorted(self.weights.items())])

class StaticModel(LinearModel):
    def __init__(self):
        self.weights = Counter()
        self.sheepWeights()

    def update(self, features, residual, stepsize):
        pass

    def targetWeights(self):
        self.weights['run:target_ahead'] = 1
        self.weights['left:a_diff'] = 0.5
        self.weights['right:a_diff'] = -0.5

    def sheepWeights(self):
        self.weights['angle=0:left'] = 1
        self.weights['angle=1:left'] = 1
        self.weights['angle=2:left'] = 1
        self.weights['angle=3:left'] = 1
        self.weights['angle=4:towards'] = 1
        self.weights['angle=5:right'] = 1
        self.weights['angle=6:right'] = 1
        self.weights['angle=7:right'] = 1
        self.weights['angle=8:right'] = 1


class NeuralModel(Model):
    ''' Use a Neural network for Q-learning '''
    def __init__(self, hidden_nodes=3):
        try:
            self.load()
            print 'Loading trained model'
        except IOError:
            print 'Cant load traint model, using new model'
            self.network = rectifier_network(hidden_nodes)

    def eval(self, features):
        return self.network.predict(features)

    def update(self, features, residual, stepsize):
        self.network.update(features, residual, stepsize)

    def save(self, filen=None):
        if filen == None:
            filen = self.__class__.__name__
        with open('{}.pkl'.format(filen), 'w') as f:
            pickle.dump(self.network, f)

    def load(self, filen=None):
        if filen == None:
            filen = self.__class__.__name__
        with open('{}.pkl'.format(filen), 'r') as f:
            self.network = pickle.load(f)
