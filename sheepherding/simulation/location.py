from math import atan2, cos, sin

class Location:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def distance(self, other):
        ''' return distance between self and other location '''
        dx = other.x - self.x
        dy = other.y - self.y
        return (dx**2 + dy**2)**0.5

    def angle(self, other):
        ''' return angle between self and other location '''
        dx = other.x - self.x
        dy = other.y - self.y
        return atan2(dy, dx)

    def da(self, other):
        ''' return distance (d) and angle (a) in a tuple '''
        dx = other.x - self.x
        dy = other.y - self.y
        return (dx**2 + dy**2)**0.5, atan2(dy, dx)

    def move(self, distance, angle):
        ''' get new location by moving distance in direction angle '''
        dx = distance * cos(angle)
        dy = distance * sin(angle)
        return Location(self.x + dx, self.y + dy)
