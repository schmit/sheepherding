'''
A small Neural Network implementation.
Note that since we are training using only residual, this module isn't that useful for other applications.

Here we use a list representation of features where each element of list corresponds to (key, value).
This helps with using very sparse features

'''

import random
from math import exp

class NeuralNetwork:
    ''' One hidden layer neural network '''
    def __init__(self, regularization=0.000001):
        self.layer = []
        self.weights = []
        self.updates = 0
        self.bias = 0
        self.regularization = regularization

    def add_unit(self, unit):
        self.layer.append(unit)
        # initialize with random weight
        self.weights.append(2*(random.random()-0.5))

    def compute_activations(self, features):
        activations = []
        for unit in self.layer:
            activations.append(unit.compute_output(features))
        return activations

    def predict(self, features):
        activations = self.compute_activations(features)
        return self.bias + sum(value * self.weights[index] for (index, value) in enumerate(activations))

    def update(self, features, residual, stepsize=0.001):
        self.updates += 1
        # update bias
        self.bias -= stepsize * -residual

        # update weights and units
        activations = self.compute_activations(features)
        for index, activation in enumerate(activations):
            partial = -residual * activation
            self.weights[index] -= stepsize * partial + self.regularization * self.weights[index]
            self.layer[index].update_weights(features, partial, stepsize)


class Unit:
    def __init__(self, regularization=0.000001):
        self.weights = {}
        self.bias = self.random_weight()
        self.regularization = regularization

    def compute_output(self, features):
        wx = self.wx(features)
        return self.f(wx)

    def wx(self, features):
        ''' compute inner product of weights and features '''
        wx = 0
        for key, value in features:
            if key not in self.weights:
                self.weights[key] = self.random_weight()
            wx += value * self.weights[key]
        return wx + self.bias

    def update_weights(self, features, partial, stepsize):
        # update bias
        self.bias -= stepsize * partial

        # update weights
        derivatives = self.df(features)
        for key, derivative in derivatives:
            gradient = partial * derivative
            self.weights[key] -= stepsize * gradient + self.regularization * self.weights[key]

    def random_weight(self):
        return (random.random() - 0.5)

    def f(self, outcome):
        '''Compute the activation function'''
        raise NotImplementedError

    def df(self, features, residual):
        '''Compute the derivative of the activation function'''
        raise NotImplementedError


class LinearUnit(Unit):
    def f(self, wx):
        ''' Linear unit: f(x) = x '''
        return wx

    def df(self, features):
        derivatives = {}
        for key, value in features:
            derivatives.append((key, value))
        return derivatives


class RectifierUnit(Unit):
    def f(self, wx):
        ''' Rectifier unit: f(x) = max(0, x) '''
        return max(0, wx)

    def df(self, features):
        derivatives = []
        if self.compute_output(features) > 0:
            for key, value in features:
                derivatives.append((key, value))
        return derivatives


class SigmoidUnit(Unit):
    def f(self, wx):
        ''' Sigmoid unit: f(x) = 1/(1+e^-x) '''
        return 1.0 / (1.0 + exp(-wx))

    def df(self, features):
        wx = self.wx(features)
        outcome = self.f(wx)
        derivatives = []
        if self.compute_output(features) > 0:
            for key, value in features:
                derivatives.append((key, value * outcome * (1-outcome)))
        return derivatives


# helper functions to easily instantiate networks
def rectifier_network(nUnits):
    network = NeuralNetwork()
    for _ in xrange(nUnits):
        network.add_unit(RectifierUnit())
    return network

def sigmoid_network(nUnits):
    network = NeuralNetwork()
    for _ in xrange(nUnits):
        network.add_unit(SigmoidUnit())
    return network
