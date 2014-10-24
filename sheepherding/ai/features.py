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
    '''
    feature extractor that computes distance and angle difference to target location
    '''
    def __call__(self, state, action):
        self.precomputation(state, action)

        result = []
        # constant
        result.append(('{}'.format(action), 1))

        # distance to target
        result.append((self.key('recip_d_target'), 2.0/(self.d_target + 1.0)))

        # in range of target
        if self.d_target < state.target_radius:
            result.append((self.key('in_range'), 1))

        # angle to target
        result.append((self.key('a_diff'), self.a_diff))

        # is target in front, left, behind or right of dog
        if self.is_target_ahead(): result.append((self.key('target_ahead'), 1))
        if self.is_target_left(): result.append((self.key('target_left'), 1))

        return result

    def precomputation(self, state, action):
        self.action = action
        self.state = state
        self.own_location = Location(state.own_location[0], state.own_location[1])
        self.d_target, self.a_target = self.own_location.da(state.target_location)
        self.a_diff = angle_difference(state.own_angle, self.a_target)

    def is_target_ahead(self):
        return -pi/2 < self.a_diff < pi/2

    def is_target_left(self):
        return self.a_diff > 0
