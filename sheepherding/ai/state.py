from ..world.location import Location

from math import pi

class State:
    '''
    Holds state of the world:

    Own location
    Sheep locations
    Other dogs locations
    Target location
    Target radius
    '''
    def __init__(self, dog, ai):
        self.own_location = (dog.loc.x, dog.loc.y)
        self.own_speed = dog.speed
        self.own_angle = dog.angle
        self.time = dog.world.iteration / 30.0

        self.sheep_locations = [(sheep.loc.x, sheep.loc.y) for sheep in dog.world.sheeps]
        self.dogs_locations = [(other_dog.loc.x, other_dog.loc.y) for other_dog in dog.world.dogs if dog is not other_dog]
        self.target_location = (dog.world.target.x, dog.world.target.y)
        self.target_radius = dog.world.target_radius

        self.sheep_done = ai.sheep_done

        # compute basic features
        self.prefeatures(dog)

    def prefeatures(self, dog):
        ''' some basic features are added to state to avoid extra computation '''
        # def is_sheep_in_target(sheep, target_location, target_radius):
        #     if sheep.loc.distance(target_location) < target_radius:
        #         return True
        #     return False

        self.target_d, self.target_a = dog.loc.da(dog.world.target)

        # Precomputation for sheep
        # only consider sheep not in target
        feasible_sheep = [(sheep_ix, sheep) for sheep_ix, sheep in enumerate(dog.world.sheeps) if sheep_ix not in self.sheep_done]
        # just in case
        if len(feasible_sheep) == 0:
            feasible_sheep = enumerate(dog.world.sheeps)
        # sort based on distance to dog
        self.sorted_sheep = sorted([(dog.loc.da(sheep.loc), sheep_ix, sheep) for sheep_ix, sheep in feasible_sheep])

        # closest sheep
        closest_sheep = self.sorted_sheep[0][1]
        self.sheep_d, self.sheep_a = dog.loc.da(dog.world.sheeps[closest_sheep].loc)
        self.sheep_t_d, self.sheep_t_a = dog.world.sheeps[closest_sheep].loc.da(dog.world.target)

    def details(self):
        ''' print details of state useful for interpretation '''
        print 'State:'
        print '='*20
        print '- dog'
        print '-'*10
        print 'location: {}'.format(self.own_location)
        print 'angle:    {}pi'.format(self.own_angle/pi)

        print '-'*10
        print '- target'
        print '-'*10
        print 'distance: {}'.format(self.target_d)
        print 'angle:    {}pi'.format(self.target_a/pi)

        print '-'*10
        print '- sheep'
        print '-'*10
        print 'distance: {}'.format(self.sheep_d)
        print 'angle:    {}pi'.format(self.sheep_a/pi)

        print '-'*10
        print '- sheep - target'
        print '-'*10
        print 'distance: {}'.format(self.sheep_t_d)
        print 'angle:    {}pi'.format(self.sheep_t_a/pi)

    def __iter__(self):
        for attr, value in self.__dict__.iteritems():
            yield attr, value

    def __repr__(self):
        return '\n'.join('{:30s}{}'.format(k, v) for k, v in self)
