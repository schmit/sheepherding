from math import atan2, cos, sin

class Location:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def distance(self, other):
        ''' return distance between self and other location '''
        # extract x and y coordinates
        if type(other) == type((1, )):
            ox = other[0]
            oy = other[1]
        else:
            # assume other is also Location
            ox = other.x
            oy = other.y
        dx = ox- self.x
        dy = oy - self.y
        return (dx**2 + dy**2)**0.5

    def angle(self, other):
        ''' return angle between self and other location '''
        # extract x and y coordinates
        if type(other) == type((1, )):
            ox = other[0]
            oy = other[1]
        else:
            # assume other is also Location
            ox = other.x
            oy = other.y
        dx = ox- self.x
        dy = oy - self.y
        return atan2(dy, dx)

    def da(self, other):
        ''' return distance (d) and angle (a) in a tuple '''
        # extract x and y coordinates
        if type(other) == type((1, )):
            ox = other[0]
            oy = other[1]
        else:
            # assume other is also Location
            ox = other.x
            oy = other.y
        # compute difference
        dx = ox - self.x
        dy = oy - self.y
        return (dx**2 + dy**2)**0.5, atan2(dy, dx)

    def dat(self, t):
        ''' return distance (d) and angle (a) in a tuple, where t is a tuple with x and y coordinates '''
        dx = t[0] - self.x
        dy = t[1] - self.y
        return (dx**2 + dy**2)**0.5, atan2(dy, dx)

    def move(self, distance, angle):
        ''' get new location by moving distance in direction angle '''
        dx = distance * cos(angle)
        dy = distance * sin(angle)
        return Location(self.x + dx, self.y + dy)
