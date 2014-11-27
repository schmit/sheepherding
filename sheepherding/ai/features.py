from ..world.location import Location
from sheepherding.util import sign, angle_difference

from math import pi, acos, tan, sin, cos

class FeatureExtractor:
    '''
    Sample feature extractor, in this case simply the identity
    '''
    def __call__(self, state, action):
        self.action = action

        result = []
        feature_key = (state, action)
        feature_value = 1
        result.append((feature_key, feature_value))
        return result

    def key(self, string):
        return '{}:{}'.format(self.action, string)


class TargetFeature(FeatureExtractor):
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
        # result.append((self.key('target_ahead'), self.is_target_ahead()))

        return result

    def precomputation(self, state, action):
        self.state = state
        self.own_location = Location(state.own_location[0], state.own_location[1])
        self.d_target, self.a_target = self.own_location.da(state.target_location)
        self.a_diff = angle_difference(state.own_angle, self.a_target)

    def is_target_ahead(self):
        return -pi/6 < self.a_diff < pi/6


class SheepFeature(FeatureExtractor):
    def __call__(self, state, action):
        self.action = action
        result = []

        # constant
        result.append((self.key('constant'), 1.0))

        # angle
        result.append((self.key('target_dog_sheep_a'), angle_difference(state.target_a, state.min_sheep_a)))
        # result.append((self.key('cos_target_dog_sheep_a'), cos(angle_difference(state.min_sheep_a, state.target_a))))
        # result.append((self.key('sin_target_dog_sheep_a'), sin(angle_difference(state.min_sheep_a, state.target_a))))

        # distance
        result.append((self.key('distance_sheep'), 2.0/(1.0+state.min_sheep_d)))
        result.append((self.key('distance_target'), 2.0/(1.0+state.min_sheep_t_d)))

        # interaction
        result.append((self.key('a*distance_sheep'), angle_difference(state.target_a, state.min_sheep_a)/(1.0+state.min_sheep_d)))
        result.append((self.key('a*distance_target'), angle_difference(state.target_a, state.min_sheep_a)/(1.0+state.min_sheep_t_d)))


        return result

