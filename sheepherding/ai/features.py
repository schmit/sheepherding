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


class TargetFeature(FeatureExtractor):
    '''
    feature extractor that computes distance and angle difference to target location
    '''
    def __call__(self, state, action):
        result = []
        own_location = Location(state.own_location[0], state.own_location[1])
        distance_to_target, angle_to_target = own_location.da(state.target_location)

        # constant
        result.append(('action:{}'.format(action), 1))

        # find the difference in angle
        angle_diff = angle_difference(state.own_angle, angle_to_target)
        # distance to target
        # result.append(('action{}-distance_to_target'.format(action), distance_to_target))
        result.append(('reciprocal_distance_to_target', 1.0/distance_to_target))
        if distance_to_target < state.target_radius:
            result.append(('distance_in_range', 1))

        # angle to target
        result.append(('action:{}-anglediff'.format(action), angle_diff))

        return result
