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
        self.sheep_locations = [(sheep.loc.x, sheep.loc.y) for sheep in dog.world.sheeps]
        self.dogs_locations = [(other_dog.loc.x, other_dog.loc.y) for dogs in dog.world.dogs if dog is not other_dog]
        self.target_location = (dog.world.target.loc.x, dog.world.target.loc.y)
        self.target_radius = dog.world.target_radius