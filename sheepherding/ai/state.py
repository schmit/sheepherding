from ..world.location import Location

class State:
    '''
    Holds state of the world:

    Own location
    Sheep locations
    Other dogs locations
    Target location
    Target radius
    '''
    def __init__(self, dog):
        self.own_location = (dog.loc.x, dog.loc.y)
        self.own_speed = dog.speed
        self.own_angle = dog.angle
        self.time = dog.world.iteration / 30.0

        self.sheep_locations = [(sheep.loc.x, sheep.loc.y) for sheep in dog.world.sheeps]
        self.dogs_locations = [(other_dog.loc.x, other_dog.loc.y) for other_dog in dog.world.dogs if dog is not other_dog]
        self.target_location = (dog.world.target.x, dog.world.target.y)
        self.target_radius = dog.world.target_radius

        # compute basic features
        self.prefeatures(dog)

    def prefeatures(self, dog):
        ''' some basic features are added to state to avoid extra computation '''
        closest_sheep = min((dog.loc.distance(sheep.loc), sheep_ix) for sheep_ix, sheep in enumerate(dog.world.sheeps))[1]
        self.min_sheep_d, self.min_sheep_a = dog.loc.da(dog.world.sheeps[closest_sheep].loc)
        self.target_d, self.target_a = dog.loc.da(dog.world.target)
        self.min_sheep_t_d, self.min_sheep_t_a = dog.world.sheeps[closest_sheep].loc.da(dog.world.target)