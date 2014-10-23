from math import pi
from ..world.location import Location

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
        result.append(('action{}-distance_to_target'.format(action), distance_to_target))
        result.append(('action{}-angle_difference'.format(action), (state.own_angle - angle_to_target) % (2*pi)))
        print 'feature: {}'.format(result)
        return result