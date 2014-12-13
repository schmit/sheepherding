from ..world.location import Location
from sheepherding.util import sign, angleDifference, binValue

from collections import Counter

from math import pi, acos, tan, sin, cos, sqrt

class FeatureExtractor:
    '''
    Sample feature extractor, in this case simply the identity
    '''
    def __call__(self, state, action):
        '''
        __call__ should return a list with features in a sparse format.
        Here, a feature is given by a tuple (key, value) where key is the
        name of the feature and value is the value of that key.

        If a key is not present, the value is assumed to be 0.
        '''
        self.action = action

        result = []
        feature_key = (state, action)
        feature_value = 1
        result.append((feature_key, feature_value))
        return result

    def key(self, string):
        '''
        format feature key name such that it includes the action and a
        string that gives the name for the feature
        '''
        return '{}:{}'.format(string, self.action)


class TargetFeature(FeatureExtractor):
    '''
    Features for moving to a target

    (deprecated: does not work in the sheepcentric world)
    '''
    def __call__(self, state, action):
        self.action = action
        self.precomputation(state, action)

        result = []

        # distance to target
        result.append(('d_target', 2.0 / (1.0 + self.d_target)))
        if self.d_target < state.target_radius:
            result.append(('in_range', 1))

        # angle difference with target
        result.append((self.key('a_diff_target'), self.a_diff))
        # result.append((self.key('target_ahead'), self.isTargetAhead()))

        return result

    def precomputation(self, state, action):
        self.state = state
        self.own_location = Location(state.own_location[0], state.own_location[1])
        self.d_target, self.a_target = self.own_location.da(state.target_location)
        self.a_diff = angleDifference(state.own_angle, self.a_target)

    def isTargetAhead(self):
        return -pi/6 < self.a_diff < pi/6


class SheepFeature(FeatureExtractor):
    '''
    Features for moving sheep to target location.
    '''
    def __call__(self, state, action):
        self.action = action
        result = []

        d_sheep = state.sheep_d
        d_target = state.target_d
        d_sheep_target = state.sheep_t_d

        # constant
        result.append((self.key('constant'), 1.0))

        # result += self.closestSheepFeature(state)
        result += self.allSheepFeature(state, 3, 3)
        result += self.allDogsFeature(state, 3, 3)
        result += self.allSheepFeature(state)
        # result += self.allSheepDTargetFeature(state)

        return result

    def closestSheepFeature(self, state):
        '''
        compute feature regarding the closest sheep
        '''
        result = []

        numbins_angle = 9 # odd is better
        numbins_dist = 10
        nbins_max_dist = 300

        d_sheep = state.sheep_d
        d_target = state.target_d

        # angle
        angle_dst = angleDifference(state.target_a, state.sheep_a)
        # binned
        angle_bin = binValue(angle_dst, numbins_angle, -pi, pi)
        result.append((self.key('angle={}'.format(angle_bin)), 1))
        # raw
        # result.append((self.key('target_dog_sheep_a'), angleDifference(state.target_a, state.sheep_a)))

        # distance
        # sheep_d_bin = binValue(sqrt(d_sheep), numbins_dist, 0, sqrt(nbins_max_dist))
        # sheep_target_d_bin = binValue(sqrt(state.sheep_t_d), numbins_dist, 0, sqrt(nbins_max_dist))

        # result.append((self.key('d_sheep={}'.format(sheep_d_bin)), 1))
        # result.append((self.key('d_sheep_target={}'.format(sheep_target_d_bin)), 1))

        # crossterms
        # result.append((self.key('da_sheep={}-{}'.format(sheep_d_bin, angle_bin)), 1))
        # result.append((self.key('da_target={}-{}'.format(sheep_target_d_bin, angle_bin)), 1))

        return result

    def allSheepFeature(self, state, nbins_dist=5, nbins_angle=9, nbins_sheep_dist=3, K=4):
        '''
        Add features for the closest K sheep:

        - binned angle difference
        - binned distance
        '''
        result = Counter()
        # initialize bin settings

        nbins_max_dist = 300
        for k, ((distance, angle), _, sheep) in enumerate(state.sorted_sheep):
            # only consider closest sheep
            if k >= K: break
            sheep_distance = sheep.loc.distance(state.target_location)
            angle_diff = angleDifference(state.target_a, angle)
            angle_bin = binValue(angle_diff, nbins_angle, -pi, pi)
            distance_bin = binValue(sqrt(distance), nbins_dist, 0, sqrt(nbins_max_dist))
            sheep_distance_bin = binValue(sqrt(sheep_distance), nbins_sheep_dist, 0, sqrt(nbins_max_dist))
            result[self.key('sheep{}_da_bins{}{}={}-{}'.format(k, nbins_dist, nbins_angle, distance_bin, angle_bin))] += 1

        return result.items()

    def allSheepDTargetFeature(self, state, nbins_sheep_dist=3):
        '''
        Bins the distance to target for every sheep
        '''
        result = Counter()
        # initialize bin settings

        nbins_max_dist = 300
        for k, ((distance, angle), _, sheep) in enumerate(state.sorted_sheep):
            # only consider closest sheep
            if k > 4: break
            sheep_distance = sheep.loc.distance(state.target_location)
            sheep_distance_bin = binValue(sqrt(sheep_distance), nbins_sheep_dist, 0, sqrt(nbins_max_dist))

            result['sheep{}_dtarget_bin={}'.format(k, sheep_distance_bin)] += 1

        return result.items()

    def allDogsFeature(self, state, nbins_dist=4, nbins_angle=7):
        '''
        add locations of other dogs

        note this feature is sheepcentric
        '''
        result = Counter()
        # initialize bin settings
        nbins_angle = 7
        nbins_dist = 7
        nbins_max_dist = 300
        for dog in state.dogs_locations:
            distance, angle = Location(state.own_location[0], state.own_location[1]).da(dog)
            angle_diff = angleDifference(state.sheep_a, angle)
            angle_bin = binValue(angle_diff, nbins_angle, -pi, pi)
            distance_bin = binValue(sqrt(distance), nbins_dist, 0, sqrt(nbins_max_dist))
            result[self.key('dog_da_bins{}{}={}-{}'.format(nbins_dist, nbins_angle, distance_bin, angle_bin))] += 1

        return result.items()

