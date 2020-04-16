import random

def random_position(dims, walls):
    r,c = dims
    pos = (random.randint(0,r-1), random.randint(0,c-1))
    while(pos in walls):
        pos = (random.randint(0,r-1), random.randint(0,c-1))
    return pos