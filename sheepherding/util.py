from math import pi

def sign(x):
    ''' returns sign of x '''
    if x > 0: return 1
    elif x < 0: return -1
    return 0

def running_avg(seq):
    ''' compute running average of sequence '''
    def gen(seq):
        total = 0.0
        count = 0
        for elem in seq:
            total += elem
            count += 1
            yield total / count
    return [x for x in gen(seq)]

def angle_difference(a, b):
    ''' compute the difference in angle between a and b '''
    raw_diff = a - b
    diff = (raw_diff + pi) % (2*pi) - pi
    return diff