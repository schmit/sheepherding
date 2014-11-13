from ..world.location import Location
from sheepherding.util import sign, angle_difference

from math import pi

class FeatureExtractor:
    '''
    Sample feature extractor, in this case simply the identity
    '''
    def __call__(self, state, action):
        result = []
        feature_key = (state, action)
        feature_value = 1
        result.append((feature_key, feature_value))
        return result

    def key(self, string):
        return '{}:{}'.format(self.action, string)


class TargetFeature(FeatureExtractor):
    def __call__(self, state, action):
        self.precomputation(state, action)

        result = []

        # distance to target
        result.append(('d_target', 2.0 / (1.0 + self.d_target)))
        if self.d_target < state.target_radius:
            result.append(('in_range', 1))

        # angle difference with target
        result.append((self.key('a_diff'), self.a_diff))
        result.append((self.key('target_ahead'), self.is_target_ahead()))

        return result

    def precomputation(self, state, action):
        self.action = action
        self.state = state
        self.own_location = Location(state.own_location[0], state.own_location[1])
        self.d_target, self.a_target = self.own_location.da(state.target_location)
        self.a_diff = angle_difference(state.own_angle, self.a_target)

    def is_target_ahead(self):
        return -pi/6 < self.a_diff < pi/6
