import random

def random_position(dims):
    r,c = dims
    return (random.randint(0,r-1), random.randint(0,c-1))