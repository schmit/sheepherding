def sign(x):
    if x > 0: return 1
    elif x < 0: return -1
    return 0

def running_avg(seq):
    def gen(seq):
        total = 0.0
        count = 0
        for elem in seq:
            total += elem
            count += 1
            yield total / count
    return [x for x in gen(seq)]